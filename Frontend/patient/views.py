"""Views for the patient app: home page and patient search."""

import logging
import math
import re
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .services import patient_service

logger = logging.getLogger(__name__)

PAGE_SIZE = 10
MIN_ID_DIGITS = 1
MAX_ID_DIGITS = 4
ADDRESS_PARTS_WITH_ORT = 2
VALID_QUERY_PATTERN = r"^[a-zA-ZäöüÄÖÜß0-9\s\-]+$"
BACKEND_ERRORS = (RuntimeError, ConnectionError, OSError, ValueError)


def home_view(request: HttpRequest) -> HttpResponse:
    """Render the home/landing page."""
    return render(request, "patient/home.html")


def _default_context() -> dict[str, Any]:
    """Liefert die Default-Werte für das Such-Template."""
    return {
        "query": "",
        "id_val": "",
        "nachname_val": "",
        "html_table": None,
        "total_count": 0,
        "current_page": 0,
        "prev_page": -1,
        "next_page": 1,
        "has_next": False,
        "filter_type": "Kein Filter",
        "error_type": "",
        "error_message": "",
        "backend_error": False,
    }


def _parse_page(request: HttpRequest) -> int:
    """Liest den Pagination-Parameter `page` robust aus der Query aus."""
    try:
        return max(0, int(request.GET.get("page", 0)))
    except ValueError, TypeError:
        return 0


def _fetch_page(*, nachname: str, page: int) -> tuple[int, str, int, bool]:
    """Holt eine Ergebnisseite vom Backend, optional nach Nachname gefiltert."""
    total_elements = patient_service.get_count(nachname=nachname)
    total_pages = math.ceil(total_elements / PAGE_SIZE) if total_elements > 0 else 1
    if page >= total_pages:
        page = max(0, total_pages - 1)

    html_table = patient_service.get_all_html(
        nachname=nachname, page=page, size=PAGE_SIZE
    )
    has_next = (page + 1) < total_pages
    return total_elements, html_table, page, has_next


def _extract_match(pattern: str, backend_html: str, default: str = "") -> str:
    """Sucht `pattern` im Backend-HTML und liefert die erste Gruppe (oder `default`)."""
    match = re.search(pattern, backend_html, re.IGNORECASE)
    return match.group(1).strip() if match else default


def _extract_address(backend_html: str) -> tuple[str, str]:
    """Extrahiert PLZ und Ort aus dem Adressfeld des Backend-HTML."""
    adresse = _extract_match(r"<strong>Adresse:</strong>\s*([^<]+)", backend_html)
    if not adresse:
        return "", ""

    adresse_parts = adresse.split(" ", 1)
    if len(adresse_parts) == ADDRESS_PARTS_WITH_ORT:
        return adresse_parts[0], adresse_parts[1]
    return adresse, ""


def _build_id_result_table(backend_html: str, query: str) -> str:
    """Parst das Backend-<article> per Regex und baut die gewohnte HTML-Tabelle."""
    fields = {
        "patient_id": _extract_match(r"<h2>Patient\s+(\d+)</h2>", backend_html, query),
        "nachname": _extract_match(
            r"<strong>Nachname:</strong>\s*([^<]+)", backend_html
        ),
        "email": _extract_match(r"<strong>E-Mail:</strong>\s*([^<]+)", backend_html),
        "geburtsdatum": _extract_match(
            r"<strong>Geburtsdatum:</strong>\s*([^<]+)", backend_html
        ),
        "geschlecht": _extract_match(
            r"<strong>Geschlecht:</strong>\s*([^<]+)", backend_html
        ),
        "familienstand": _extract_match(
            r"<strong>Familienstand:</strong>\s*([^<]+)", backend_html
        ),
    }
    fields["plz"], fields["ort"] = _extract_address(backend_html)

    return f"""
    <table>
        <thead>
            <tr>
                <th>ID</th><th>Nachname</th><th>E-Mail</th><th>Geburtsdatum</th>
                <th>Geschlecht</th><th>Familienstand</th><th>PLZ</th><th>Ort</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>{fields["patient_id"]}</td>
                <td>{fields["nachname"]}</td>
                <td>{fields["email"]}</td>
                <td>{fields["geburtsdatum"]}</td>
                <td>{fields["geschlecht"]}</td>
                <td>{fields["familienstand"]}</td>
                <td>{fields["plz"]}</td><td>{fields["ort"]}</td>
            </tr>
        </tbody>
    </table>
    """


def _render_validation_error(
    request: HttpRequest, query: str, id_val: str, nachname_val: str, message: str
) -> HttpResponse:
    """Rendert das Such-Template mit einer Validierungsfehlermeldung."""
    context = _default_context()
    context.update(
        query=query,
        id_val=id_val,
        nachname_val=nachname_val,
        filter_type="Ungültig",
        error_type="validation_error",
        error_message=message,
    )
    return render(request, "patient/search.html", context)


def _search_unfiltered(
    request: HttpRequest, id_val: str, nachname_val: str
) -> HttpResponse:
    """Leere Gesamtsuche ohne Filter, aber mit Pagination."""
    page = _parse_page(request)
    html_table, total_elements, has_next, backend_error = "", 0, False, False
    try:
        total_elements, html_table, page, has_next = _fetch_page(nachname="", page=page)
    except BACKEND_ERRORS as exc:
        logger.error("Backend request failed: %s", exc)
        backend_error = True

    context = _default_context()
    context.update(
        id_val=id_val,
        nachname_val=nachname_val,
        html_table=html_table,
        total_count=total_elements,
        current_page=page,
        prev_page=page - 1,
        next_page=page + 1,
        has_next=has_next,
        backend_error=backend_error,
    )
    return render(request, "patient/search.html", context)


def _search_by_id(
    request: HttpRequest, query: str, id_val: str, nachname_val: str
) -> HttpResponse:
    """ID-Suche (reine Ziffern), ohne Pagination."""
    if not (MIN_ID_DIGITS <= len(query) <= MAX_ID_DIGITS):
        return _render_validation_error(
            request,
            query,
            id_val,
            nachname_val,
            "Die ID muss zwischen 1 und 4 Ziffern lang sein.",
        )

    html_table, total_elements, backend_error = "", 0, False
    try:
        backend_html = patient_service.get_by_id_html(int(query))
        if backend_html:
            html_table = _build_id_result_table(backend_html, query)
            total_elements = 1
    except BACKEND_ERRORS as exc:
        logger.error("Backend request failed: %s", exc)
        backend_error = True

    context = _default_context()
    context.update(
        query=query,
        id_val=id_val,
        nachname_val=nachname_val,
        html_table=html_table,
        total_count=total_elements,
        filter_type="ID",
        backend_error=backend_error,
    )
    return render(request, "patient/search.html", context)


def _search_by_nachname(
    request: HttpRequest, query: str, id_val: str, nachname_val: str
) -> HttpResponse:
    """Nachname-Suche (Buchstaben), mit Pagination."""
    page = _parse_page(request)
    html_table, total_elements, has_next, backend_error = "", 0, False, False
    try:
        total_elements, html_table, page, has_next = _fetch_page(
            nachname=query, page=page
        )
    except BACKEND_ERRORS as exc:
        logger.error("Backend request failed: %s", exc)
        backend_error = True

    context = _default_context()
    context.update(
        query=query,
        id_val=id_val,
        nachname_val=nachname_val,
        html_table=html_table,
        total_count=total_elements,
        current_page=page,
        prev_page=page - 1,
        next_page=page + 1,
        has_next=has_next,
        filter_type="Nachname",
        backend_error=backend_error,
    )
    return render(request, "patient/search.html", context)


def search_view(request: HttpRequest) -> HttpResponse:
    """Handle patient search: by ID, by Nachname, or unfiltered with pagination."""
    id_val = request.GET.get("id", "").strip()
    nachname_val = request.GET.get("nachname", "").strip()
    query_val = request.GET.get("query", "").strip()

    # Einheitlichen Suchbegriff ermitteln, je nachdem welches Feld gefüllt ist
    query = id_val or nachname_val or query_val

    # Prüfen, ob überhaupt ein Such-Event stattgefunden hat (Parameter in request.GET)
    if not any(k in request.GET for k in ("id", "nachname", "query")):
        return render(request, "patient/search.html", _default_context())

    if not query:
        return _search_unfiltered(request, id_val, nachname_val)

    if not re.match(VALID_QUERY_PATTERN, query):
        return _render_validation_error(
            request,
            query,
            id_val,
            nachname_val,
            "Ungültige Zeichen verwendet. Bitte nur Buchstaben oder Zahlen eingeben.",
        )

    if query.isdigit():
        return _search_by_id(request, query, id_val, nachname_val)

    return _search_by_nachname(request, query, id_val, nachname_val)
