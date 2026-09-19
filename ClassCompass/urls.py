"""
URL configuration for ClassCompass project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from courses import views

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path(
        "calendar/<int:primary_key>/",
        views.CalendarView.as_view(),
        name="calendar"
    ),
    path("courses/", views.course_list_view, name="course_list"),
    path(
        "courses/add/",
        views.CourseCreateView.as_view(),
        name="course_create"
    ),
    path(
        "courses/<int:primary_key>/",
        views.CourseDetailView.as_view(),
        name="course_detail"
    ),
    path(
        "courses/<int:primary_key>/edit/",
        views.CourseUpdateView.as_view(),
        name="course_update"
    ),
    path(
        "courses/<int:primary_key>/delete/",
        views.CourseDeleteView.as_view(),
        name="course_delete"
    ),
    path(
        "syllabi/",
        views.SyllabusListView.as_view(),
        name="syllabus_list"
    ),
    path(
        "syllabi/upload/",
        views.SyllabusUploadView.as_view(),
        name="syllabus_upload"
    ),
    path(
        "events/<int:primary_key>/",
        views.EventDetailView.as_view(),
        name="event_detail"
    ),
    path(
        "events/add/",
        views.EventCreateView.as_view(),
        name="event_create"
    ),
    path(
        "events/<int:primary_key>/edit/",
        views.EventUpdateView.as_view(),
        name="event_update"
    ),
    path(
        "events/<int:primary_key>/delete/",
        views.EventDeleteView.as_view(),
        name="event_delete"
    ),
]
