from django.contrib import admin
from django.urls import include, path

from courses.views import redirect_root_view

urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "",
        include("courses.urls"),
    ),
]