from django.urls import path

from . import views


app_name = "courses"


urlpatterns = [
    # path('', views.redirect_root_view()),

    path(
        "courses/summary/",
        views.course_summary_view,
        name="course_summary",
    ),

    path(
        "courses/",
        views.course_list_view,
        name="course_list",
    ),

    path(
        "courses/overview/",
        views.CourseOverviewView.as_view(),
        name="course_overview",
    ),

    path(
        "courses/<int:pk>/",
        views.CourseDetailView.as_view(),
        name="course_detail",
    ),


    path(
        "",
        views.DashboardView.as_view(),
        name="dashboard",
    ),

    path(
        "calendar/",
        views.CalendarView.as_view(),
        name="calendar",
    ),

    path(
        "courses/add/",
        views.CourseCreateView.as_view(),
        name="course_create",
    ),

    path(
        "courses/<int:pk>/edit/",
        views.CourseUpdateView.as_view(),
        name="course_update",
    ),

    path(
        "courses/<int:pk>/delete/",
        views.CourseDeleteView.as_view(),
        name="course_delete",
    ),

    path(
        "syllabi/",
        views.SyllabusListView.as_view(),
        name="syllabus_list",
    ),

    path(
        "syllabi/upload/",
        views.SyllabusUploadView.as_view(),
        name="syllabus_upload",
    ),

    path(
        "events/add/",
        views.EventCreateView.as_view(),
        name="event_create",
    ),

    path(
        "events/<int:pk>/",
        views.EventDetailView.as_view(),
        name="event_detail",
    ),

    path(
        "events/<int:pk>/edit/",
        views.EventUpdateView.as_view(),
        name="event_update",
    ),

    path(
        "events/<int:pk>/delete/",
        views.EventDeleteView.as_view(),
        name="event_delete",
    ),
]