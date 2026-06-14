"""URL configuration for the Frontend project."""

from django.urls import include, path

urlpatterns = [
    path("", include("patient.urls")),
]
