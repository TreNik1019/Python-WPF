"""URL configuration for the patient app."""

from django.urls import path

from patient.views import search_view, home_view

urlpatterns = [
    path("", home_view, name="home"),
    path('search/', search_view, name='patienten_suche')
]
