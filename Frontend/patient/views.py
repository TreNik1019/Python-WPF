"""Views for the patient frontend application."""

from django.http import HttpRequest
from django.shortcuts import render

from patient.services.patient_service import get_all


def patienten_view(request: HttpRequest) -> object:
    """Render the patient list page with filtered and paginated data."""
    nachname = request.GET.get("nachname", "")
    email = request.GET.get("email", "")
    page = request.GET.get("page", 0)
    size = request.GET.get("size", 5)

    backend_error = False
    try:
        result = get_all(nachname=nachname, email=email, page=page, size=size)
    except (RuntimeError, ConnectionError, OSError):
        backend_error = True
        result = {
            "content": [],
            "page": {
                "size": 5,
                "number": 0,
                "total_elements": 0,
                "total_pages": 0,
            },
        }

    context = {
        "content": result["content"],
        "page_meta": result["page"],
        "nachname": nachname,
        "email": email,
        "backend_error": backend_error,
    }
    return render(request, "patient/liste.html", context)
