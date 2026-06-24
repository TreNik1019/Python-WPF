"""HTTP client for retrieving patient data from the FastAPI backend."""

from typing import Any
import requests
from django.conf import settings

BACKEND_URL = getattr(settings, "BACKEND_URL", "https://127.0.0.1:8000/rest")
HTTP_OK = 200


def get_all_html(nachname: str = "", page: int = 0, size: int = 10) -> str:
    """Holt die fertige HTML-Tabelle vom Backend – optional gefiltert und mit Pagination."""
    params = (
        {"page": page, "size": size, "nachname": nachname}
        if nachname
        else {"page": page, "size": size}
    )

    # Default
    # verify=False: self-signed cert in local dev -
    # must be True with valid cert in production
    response = requests.get(BACKEND_URL, params=params, timeout=10, verify=False)
    if response.status_code == HTTP_OK:
        return response.text
    return ""


def get_count(nachname: str = "") -> int:
    """Holt die Anzahl der Treffer – entweder global oder gefiltert nach Nachname."""
    params: dict[str, Any] = {"page": 0, "size": 1}
    if nachname:
        params["Nachname"] = nachname

    headers = {"Accept": "application/json"}

    # verify=False: self-signed cert in local dev -
    # must be True with valid cert in production
    response = requests.get(
        BACKEND_URL, params=params, headers=headers, timeout=10, verify=False
    )
    if response.status_code == HTTP_OK:
        data = response.json()
        return int(data.get("page", {}).get("total_elements", 0))
    return 0


def get_by_id_html(patient_id: int) -> str:
    """Ruft den spezifischen ID-Endpoint auf und liefert das HTML."""
    url = f"{BACKEND_URL}/{patient_id}"
    # verify=False: self-signed cert in local dev -
    # must be True with valid cert in production
    response = requests.get(url, timeout=10, verify=False)

    if response.status_code == HTTP_OK:
        return response.text

    return ""
