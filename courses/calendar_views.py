import json
from datetime import datetime
from decimal import Decimal, InvalidOperation

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .calendar_ai import extract_calendar_events, validate_event
from .models import AcademicEvent, Course


@login_required
@require_POST
def extract_all_events(request):
    """
    Extract calendar events from syllabus text using
    the local Hugging Face model.
    """
    try:
        if len(request.body) > 25000:
            return JsonResponse(
                {
                    "status": "error",
                    "error": "Input is too large."
                },
                status=413
            )

        data = json.loads(request.body)

        if not isinstance(data, dict):
            raise ValueError("Invalid request.")

        syllabus = data.get("syllabus", "")
        method = data.get("method", "zero_shot")

        if not isinstance(syllabus, str) or not syllabus.strip():
            raise ValueError("Syllabus cannot be empty.")

        if len(syllabus) > 20000:
            raise ValueError(
                "Maximum 20,000 characters allowed."
            )

        if method not in ("zero_shot", "few_shot"):
            raise ValueError("Invalid prompting method.")

        result = extract_calendar_events(
            syllabus,
            method=method
        )

        return JsonResponse(result)

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

    except Exception:
        return JsonResponse(
            {
                "status": "error",
                "error": "AI extraction failed. Please try again."
            },
            status=500
        )


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
