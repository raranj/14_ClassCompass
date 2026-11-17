import json
from datetime import datetime
from decimal import Decimal, InvalidOperation
import time
from pathlib import Path

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import AcademicEvent, Course, AIRequestLog
from .syllabus_files import extract_syllabus_file


@login_required
@require_POST
def extract_all_events(request):
    started = time.perf_counter()
    input_method = "text"
    syllabus_length = 0
    generated_tokens = 0
    extracted_events = 0
    status = "failure"
    try:
        uploaded_file = request.FILES.get("syllabus_file")
        if uploaded_file:
            extension = Path(uploaded_file.name).suffix.lower()
            input_method = {
                ".pdf": "pdf",
                ".docx": "docx",
                ".html": "html",
                ".htm": "html",
            }.get(extension, "text")
            syllabus = extract_syllabus_file(uploaded_file)
            method = request.POST.get("method", "zero_shot")
        elif request.content_type.startswith("application/json"):
            if len(request.body) > 25000:
                raise ValueError("Input is too large.")
            data = json.loads(request.body)
            if not isinstance(data, dict):
                raise ValueError("Invalid request.")
            syllabus = data.get("syllabus", "")
            method = data.get("method", "zero_shot")
        else:
            syllabus = request.POST.get("syllabus", "")
            method = request.POST.get("method", "zero_shot")
        if not isinstance(syllabus, str) or not syllabus.strip():
            raise ValueError(
                "Paste syllabus text or upload a supported file."
            )
        syllabus_length = len(syllabus)
        if syllabus_length > 20000:
            raise ValueError("Maximum 20,000 characters allowed.")
        if method not in ("zero_shot", "few_shot"):
            raise ValueError("Invalid prompting method.")
        from .calendar_ai import extract_calendar_events
        result = extract_calendar_events(
            syllabus,
            method=method,
        )
        generated_tokens = result.get("generated_tokens", 0)
        extracted_events = result.get("count", 0)
        status = "success"
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        result = {
            "status": "error",
            "error": str(exc),
        }
    except Exception:
        result = {
            "status": "error",
            "error": "Syllabus extraction failed.",
        }
    latency = time.perf_counter() - started
    log = AIRequestLog.objects.create(
        user=request.user,
        input_method=input_method,
        syllabus_length=syllabus_length,
        latency_seconds=round(latency, 3),
        generated_tokens=generated_tokens,
        extracted_events=extracted_events,
        status=status,
    )
    if status == "success":
        result["request_id"] = log.id
        return JsonResponse(result)

    return JsonResponse(result, status=400)


def parse_datetime(event):
    """
    Convert an event's date and time into a
    timezone-aware datetime.

    Return None for events without a specific date,
    including recurring weekly office hours.
    """
    date_string = event.get("date")

    if not date_string:
        return None

    time_string = event.get("time") or "00:00"

    parsed = datetime.strptime(
        f"{date_string} {time_string}",
        "%Y-%m-%d %H:%M"
    )

    return timezone.make_aware(
        parsed,
        timezone.get_current_timezone()
    )

@login_required
@require_POST
def save_calendar_events(request):
    """
    Save selected AI-extracted events to a course.

    Supports:
    - Assignments, quizzes, exams, and other event types
    - Multiple events in one request
    - Recurring weekly events
    - Estimated hours
    - Duplicate prevention
    - User-specific course ownership
    """
    from .calendar_ai import validate_event
    try:
        if len(request.body) > 200000:
            return JsonResponse(
                {
                    "status": "error",
                    "error": "Request is too large."
                },
                status=413
            )

        data = json.loads(request.body)

        if not isinstance(data, dict):
            raise ValueError("Invalid request.")

        course_id = data.get("course_id")
        events = data.get("events")
        request_id = data.get("request_id")
        log = AIRequestLog.objects.filter(
            id=request_id,
            user=request.user,
            status="success",
            is_simulated=False,
        ).first()

        # Only allow saving to the logged-in user's course.
        course = Course.objects.filter(
            id=course_id,
            user=request.user
        ).first()

        if course is None:
            return JsonResponse(
                {
                    "status": "error",
                    "error": "Course not found."
                },
                status=404
            )

        if not isinstance(events, list):
            raise ValueError("Events must be a list.")

        if not events:
            raise ValueError("Select at least one event.")

        if len(events) > 100:
            raise ValueError(
                "Cannot save more than 100 events at once."
            )

        # Validate all events before saving anything.
        prepared_events = []

        for raw_event in events:
            event = validate_event(raw_event)

            estimated_hours = event["estimated_hours"]

            if estimated_hours is not None:
                try:
                    estimated_hours = Decimal(
                        str(estimated_hours)
                    )

                    if estimated_hours > Decimal("9999.99"):
                        raise ValueError(
                            "Estimated hours are too large."
                        )

                except (InvalidOperation, ValueError):
                    raise ValueError(
                        "Invalid estimated hours."
                    )

            start = parse_datetime(event)
            end = None

            if event["end_time"] and event["date"]:
                end = timezone.make_aware(
                    datetime.strptime(
                        event["date"] + " " + event["end_time"],
                        "%Y-%m-%d %H:%M"
                    ),
                    timezone.get_current_timezone()
                )

            if start and end and end < start:
                raise ValueError(
                    "End time cannot be before start time."
                )

            if (
                event["repeats_weekly"]
                and event["end_time"]
                and event["time"]
                and event["end_time"] < event["time"]
            ):
                raise ValueError(
                    "Weekly event end time cannot be before start time."
                )

            prepared_events.append(
                (event, estimated_hours, start, end)
            )

        created_count = 0
        skipped_count = 0

        with transaction.atomic():

            for event, hours, start, end in prepared_events:

                weekday = event["weekday"] or ""

                # Match exact event details so Monday and
                # Wednesday office hours can both be saved.
                already_exists = AcademicEvent.objects.filter(
                    course=course,
                    title=event["title"],
                    event_type=event["event_type"],
                    scheduled_at=start,
                    repeats_weekly=event["repeats_weekly"],
                    weekday=weekday,
                    start_time=event["time"] or None
                ).exists()

                if already_exists:
                    skipped_count += 1
                    continue

                try:
                    with transaction.atomic():

                        AcademicEvent.objects.create(
                            course=course,
                            title=event["title"],
                            event_type=event["event_type"],
                            description=event["description"] or "",
                            scheduled_at=start,
                            end_at=end,
                            all_day=(
                                start is not None
                                and event["time"] is None
                            ),
                            estimated_hours=hours,
                            estimate_source=(
                                "ai"
                                if hours is not None
                                else "unknown"
                            ),
                            source="ai",
                            status="todo",
                            repeats_weekly=event["repeats_weekly"],
                            weekday=weekday,
                            start_time=event["time"] or None,
                            end_time=event["end_time"] or None
                        )

                    created_count += 1

                except IntegrityError:
                    # Handle a database uniqueness conflict.
                    skipped_count += 1
        has_office_hours = any(
            event["event_type"] == "office_hours"
            for event, hours, start, end in prepared_events
        )
        if has_office_hours:
            office_events = AcademicEvent.objects.filter(
                course=course,
                event_type="office_hours",
                repeats_weekly=True,
            ).exclude(weekday="")
            weekday_order = {
                "monday": 0,
                "tuesday": 1,
                "wednesday": 2,
                "thursday": 3,
                "friday": 4,
                "saturday": 5,
                "sunday": 6,
            }
            office_events = sorted(
                office_events,
                key=lambda e: (
                    weekday_order.get(e.weekday.lower(), 7),
                    e.start_time or datetime.min.time(),
                )
            )
            lines = []
            for office_event in office_events:
                day = office_event.weekday.capitalize()
                if office_event.start_time:
                    start_label = office_event.start_time.strftime(
                        "%I:%M %p"
                    ).lstrip("0")
                    if office_event.end_time:
                        end_label = office_event.end_time.strftime(
                            "%I:%M %p"
                        ).lstrip("0")
                        schedule = (
                            f"{day}: {start_label} - {end_label}"
                        )
                    else:
                        schedule = f"{day}: {start_label}"
                else:
                    schedule = day
                if schedule not in lines:
                    lines.append(schedule)
            marker = "AI-EXTRACTED OFFICE HOURS:"
            existing = course.office_hours or ""
            manual_text = existing.split(marker, 1)[0].strip()
            if lines:
                generated_text = (
                        marker + "\n" + "\n".join(lines)
                )
                course.office_hours = (
                    manual_text + "\n\n" + generated_text
                    if manual_text
                    else generated_text
                )
                course.save(update_fields=["office_hours"])
        if log is not None:
            with transaction.atomic():
                locked_log = AIRequestLog.objects.select_for_update().get(
                    pk=log.pk
                )
                locked_log.saved_events = min(
                    locked_log.extracted_events,
                    locked_log.saved_events + created_count,
                )
                locked_log.save(update_fields=["saved_events"])

        return JsonResponse({
            "status": "success",
            "created": created_count,
            "skipped": skipped_count,
            "message": (
                f"Added {created_count} events "
                "to your calendar."
            )
        })

    except json.JSONDecodeError:
        return JsonResponse(
            {
                "status": "error",
                "error": "Invalid JSON request."
            },
            status=400
        )

    except (ValueError, TypeError) as exc:
        return JsonResponse(
            {
                "status": "error",
                "error": str(exc)
            },
            status=400
        )
