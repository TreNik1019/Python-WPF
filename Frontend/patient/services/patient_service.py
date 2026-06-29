"""HTTP client for retrieving patient data from the FastAPI backend."""

from typing import Any

import httpx
from django.conf import settings

BACKEND_URL = getattr(settings, "BACKEND_URL", "https://127.0.0.1:8000/rest")
TLS_VERIFY = getattr(settings, "BACKEND_TLS_VERIFY", True)
HTTP_OK = 200


def _get(url: str, **kwargs: Any) -> httpx.Response:
    """Fuehrt einen GET-Request aus und normiert Client-Fehler."""
    try:
        return httpx.get(url, timeout=10, verify=TLS_VERIFY, **kwargs)
    except httpx.HTTPError as exc:
        raise ConnectionError("Backend request failed") from exc


def get_all_html(nachname: str = "", page: int = 0, size: int = 10) -> str:
    """Holt die HTML-Tabelle vom Backend, optional gefiltert und mit Pagination."""
    params = (
        {"page": page, "size": size, "nachname": nachname}
        if nachname
        else {"page": page, "size": size}
    )

    response = _get(BACKEND_URL, params=params)
    if response.status_code == HTTP_OK:
        return response.text
    return ""


def get_count(nachname: str = "") -> int:
    """Holt die Anzahl der Treffer, entweder global oder gefiltert nach Nachname."""
    params: dict[str, Any] = {"page": 0, "size": 1}
    if nachname:
        params["nachname"] = nachname

    headers = {"Accept": "application/json"}

    response = _get(BACKEND_URL, params=params, headers=headers)
    if response.status_code == HTTP_OK:
        data = response.json()
        return int(data.get("page", {}).get("total_elements", 0))
    return 0


def get_by_id_html(patient_id: int) -> str:
    """Ruft den spezifischen ID-Endpoint auf und liefert das HTML."""
    url = f"{BACKEND_URL}/{patient_id}"
    response = _get(url)

    if response.status_code == HTTP_OK:
        return response.text

    return ""
