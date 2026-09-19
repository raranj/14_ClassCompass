from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Course, Syllabus, AcademicEvent


# FBV - HTTP response
def dashboard_view(request):
    return HttpResponse("""
        <h1>ClassCompass Dashboard</h1>
        <p>Welcome to ClassCompass!</p>
        <p>Manage your courses, events, grades, and study tools.</p>
    """)


# FBV - render
def course_list_view(request):
    courses = Course.objects.filter(user=request.user)
    return render(
        request,
        "courses/course_list.html",
        {
            "courses": courses
        }
    )


# Base CBV
class CalendarView(View):
    def get(self, request, primary_key):
        event = AcademicEvent.objects.get(pk=primary_key)
        return render(
            request,
            "calendar/calendar.html",
            {
                "event": event
            }
        )

# Generic CBV
class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "course"


class CourseCreateView(CreateView):
    model = Course
    fields = [
        "course_code",
        "course_name",
        "term",
        "year",
        "office_hours",
        "meeting_schedule",
        "description",
    ]
    template_name = "courses/course_form.html"


class CourseUpdateView(UpdateView):
    model = Course
    fields = [
        "course_code",
        "course_name",
        "term",
        "year",
        "office_hours",
        "meeting_schedule",
        "description",
    ]
    template_name = "courses/course_form.html"


class CourseDeleteView(DeleteView):
    model = Course
    template_name = "courses/course_confirm_delete.html"


class SyllabusListView(ListView):
    model = Syllabus
    template_name = "courses/syllabus_list.html"


class SyllabusUploadView(View):
    model = Syllabus
    template_name = "courses/syllabus_upload.html"


class EventDetailView(DetailView):
    model = AcademicEvent
    template_name = "events/event_detail.html"
    context_object_name = "event"


class EventCreateView(CreateView):
    model = AcademicEvent
    fields = [
        "course",
        "title",
        "event_type",
        "description",
        "scheduled_at",
        "end_at",
        "all_day",
        "estimated_hours",
        "estimate_source",
        "source",
        "status",
    ]
    template_name = "events/event_form.html"


class EventUpdateView(UpdateView):
    model = AcademicEvent
    fields = [
        "course",
        "title",
        "event_type",
        "description",
        "scheduled_at",
        "end_at",
        "all_day",
        "estimated_hours",
        "estimate_source",
        "source",
        "status",
    ]
    template_name = "events/event_form.html"


class EventDeleteView(DeleteView):
    model = AcademicEvent
    template_name = "events/event_confirm_delete.html"