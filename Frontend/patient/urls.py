"""URL configuration for the patient app."""

from django.urls import path

from patient.views import patienten_view

urlpatterns = [
    path("", patienten_view, name="patienten"),
]
