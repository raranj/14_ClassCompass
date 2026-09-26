from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Course, Syllabus, AcademicEvent, StudyTool

def redirect_root_view(request):
    return redirect("dashboard")


def course_summary_view(request):
    """
    Displays a summary of the courses in ClassCompass.

    This view demonstrates the manual template-loading approach:
    1. Query the Course model
    2. Load the template manually
    3. Render the template manually with context
    4. Wrap the result in HttpResponse
    """

    courses = Course.objects.all()

    template = loader.get_template(
        "courses/course_summary.html"
    )

    context = {
        "courses": courses,
        "course_count": courses.count(),
    }

    output = template.render(context, request)

    return HttpResponse(output)

class StudyToolListView(ListView):
    """
    Displays study tools generated for courses.
    """
    model = StudyTool
    template_name = "courses/study_tool_list.html"
    context_object_name = "study_tools"

def course_list_view(request):
    """
    Displays all courses.

    This view demonstrates Django's render() shortcut:
    1. Query the Course model
    2. Put the queryset in a context dictionary
    3. Call render()
    """

    courses = Course.objects.all()


    context = {
        "courses": courses,
    }

    return render(
        request,
        "courses/course_list.html",
        context,
    )

class CourseOverviewView(View):
    def get(self, request):
        courses = Course.objects.order_by("course_code")

        context = {
            "courses": courses,
        }

        return render(
            request,
            "courses/course_list.html",
            context,
        )

class CourseDetailView(DetailView):
    """
    Displays one specific Course.

    DetailView automatically retrieves the Course specified
    by the primary key in the URL.
    """

    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "course"

class DashboardView(View):
    """
    Displays the main ClassCompass dashboard.
    """

    def get(self, request):
        courses = Course.objects.all()
        events = AcademicEvent.objects.all()

        context = {
            "courses": courses,
            "events": events,
        }

        return render(
            request,
            "dashboard/dashboard.html",
            context,
        )

class CalendarView(View):
    """
    Displays academic events in the calendar.
    """

    def get(self, request):
        events = AcademicEvent.objects.all()

        context = {
            "events": events,
        }

        return render(
            request,
            "calendar/calendar.html",
            context,
        )

class CourseCreateView(CreateView):
    """
    Creates a new Course.
    """

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

    success_url = reverse_lazy(
        "courses:course_list"
    )

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CourseUpdateView(UpdateView):
    """
    Updates an existing Course.
    """

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

    success_url = reverse_lazy(
        "courses:course_list"
    )


class CourseDeleteView(DeleteView):
    """
    Deletes an existing Course.
    """

    model = Course

    template_name = "courses/course_confirm_delete.html"

    success_url = reverse_lazy(
        "courses:course_list"
    )

class SyllabusListView(ListView):
    """
    Displays uploaded syllabi.
    """

    model = Syllabus
    template_name = "courses/syllabus_list.html"
    context_object_name = "syllabi"


class SyllabusUploadView(View):
    """
    Displays the syllabus upload page.

    The POST logic for actually processing the uploaded syllabus
    can be added when syllabus processing is implemented.
    """

    def get(self, request):
        return render(
            request,
            "courses/syllabus_upload.html",
        )


class EventDetailView(DetailView):
    """
    Displays one AcademicEvent.
    """

    model = AcademicEvent
    template_name = "events/event_detail.html"
    context_object_name = "event"


class EventCreateView(CreateView):
    """
    Creates a new AcademicEvent.
    """

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

    success_url = reverse_lazy(
        "courses:calendar"
    )


class EventUpdateView(UpdateView):
    """
    Updates an existing AcademicEvent.
    """

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

    success_url = reverse_lazy(
        "courses:calendar"
    )


class EventDeleteView(DeleteView):
    """
    Deletes an AcademicEvent.
    """

    model = AcademicEvent

    template_name = "events/event_confirm_delete.html"

    success_url = reverse_lazy(
        "courses:calendar"
    )