from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse_lazy
from django.views import View
from django.db.models import Count, Q
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .forms import CourseForm
from .models import Course, Syllabus, AcademicEvent, StudyTool
from io import BytesIO
from django.http import HttpResponse
from django.db.models import Count
from django.db.models.functions import TruncDate
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

class CourseListView(ListView):
    model = Course
    template_name = "courses/course_search.html"
    context_object_name = "course_rows_for_looping"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        q = self.request.GET.get("q")
        term = self.request.GET.get("term")

        if q:
            search_qs = Course.objects.filter(
                Q(course_code__icontains=q) | Q(course_name__icontains=q)
            )
        else:
            search_qs = Course.objects.all()

        if term:
            search_qs = search_qs.filter(term__exact=term)

        ctx["q"] = q
        ctx["term"] = term
        ctx["term_choices"] = Course.TERM_CHOICES
        ctx["search_results"] = search_qs

        ctx["total_courses"] = Course.objects.count()
        ctx["total_events"] = AcademicEvent.objects.count()

        ctx["courses_per_term"] = (
            Course.objects
            .values("term")
            .annotate(n_courses=Count("id"))
            .order_by("term")
        )

        ctx["events_per_course"] = (
            Course.objects
            .values("course_code")
            .annotate(
                n_events=Count("academicevent"),
                n_completed=Count(
                    "academicevent",
                    filter=Q(academicevent__status="completed"),
                ),
            )
            .order_by("course_code")
        )
        ctx["form"] = CourseForm()
        return ctx

    def post(self, request, *args, **kwargs):
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.save()
            return redirect("courses:course_search")
        self.object_list = self.get_queryset()
        ctx = self.get_context_data()
        ctx["form"] = form
        return self.render_to_response(ctx)


def redirect_root_view(request):
    return redirect("courses:dashboard")

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

def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.save()
            return redirect("courses:course_list")
    else:
        form = CourseForm()
    return render(request, "courses/course_form.html", {"form": form})

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


def event_search_view(request):
    if request.method == "POST":
        course_code = request.POST.get("course_code", "").strip()
        status = request.POST.get("status", "").strip()

        results_for_looping = AcademicEvent.objects.all()

        if course_code:
            results_for_looping = results_for_looping.filter(
                course__course_code__icontains=course_code
            )
        if status:
            results_for_looping = results_for_looping.filter(status__exact=status)
    else:
        results_for_looping = None
        course_code = ""
        status = ""

    return render(
        request,
        "courses/event_search.html",
        {
            "results_for_looping": results_for_looping,
            "course_code": course_code,
            "status": status,
            "status_choices": AcademicEvent.STATUS_CHOICES,
        },
    )

def course_summary_view(request):
    courses = Course.objects.all()

    courses_by_term = (
        Course.objects.values("term")
        .annotate(course_count=Count("id"))
        .order_by("term")
    )
    template = loader.get_template("courses/course_summary.html")
    context = {
        "courses": courses,
        "course_count": courses.count(),
        "courses_by_term": courses_by_term,
    }
    output = template.render(context, request)
    return HttpResponse(output)

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
    form_class = CourseForm
    template_name = "courses/course_form.html"
    success_url = reverse_lazy("courses:course_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CourseUpdateView(UpdateView):
    """
    Updates an existing Course.
    """

    model = Course
    form_class = CourseForm
    template_name = "courses/course_form.html"
    success_url = reverse_lazy("courses:course_list")


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
def academic_event_chart(request):
    events = AcademicEvent.objects.all()
    event_data = (
        events
        .annotate(event_date=TruncDate('scheduled_at'))
        .values('event_date')
        .annotate(count=Count('id'))
        .order_by('event_date')
    )
    dates = [str(item['event_date']) for item in event_data]
    counts = [item['count'] for item in event_data]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(dates, counts, color='#93c5fd', edgecolor='#1d4ed8', linewidth=1.5)
    ax.set_title('Academic Events by Date', fontsize=14, fontweight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.locator_params(axis='y', integer=True)
    ax.set_ylabel('Number\nof\nEvents', fontsize=12, rotation=0, labelpad=25)
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close(fig)
    return HttpResponse(buffer.getvalue(), content_type='image/png')
