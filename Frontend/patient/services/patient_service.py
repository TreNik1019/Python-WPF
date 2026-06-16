"""HTTP client for retrieving patient data from the FastAPI backend."""

import requests
from django.conf import settings

BACKEND_URL = getattr(settings, "BACKEND_URL", "https://127.0.0.1:8000/rest")
BACKEND_VERIFY = getattr(settings, "BACKEND_VERIFY", False)
HTTP_OK = 200

def get_all_html(page: int = 0, size: int = 10) -> str:
    """Holt die Patiententabelle als fertigen HTML-String vom Backend."""
    params = {"page": page, "size": size}

    # Standardaufruf
    response = requests.get(BACKEND_URL, params=params, timeout=10, verify=BACKEND_VERIFY)
    
    if response.status_code != HTTP_OK:
        raise RuntimeError(f"Backend-Fehler {response.status_code}: {response.text}")

    return response.text

def get_count() -> int:
    """Nutzt den Accept-Header, um die Anzahl der Patienten aus dem Backend-JSON zu lesen."""
    params = {"page": 0, "size": 1}

    headers = {"Accept": "application/json"}
    
    response = requests.get(BACKEND_URL, params=params, headers=headers, timeout=10, verify=BACKEND_VERIFY)
    
    if response.status_code == HTTP_OK:
        data = response.json()
        return int(data.get("page", {}).get("total_elements", 0))

    return 0

def get_by_id_html(patient_id: int) -> str:
    """Ruft den spezifischen ID-Endpoint auf und liefert das HTML."""
    url = f"{BACKEND_URL}/{patient_id}"
    response = requests.get(url, timeout=10, verify=BACKEND_VERIFY)
    
    if response.status_code == HTTP_OK:
        return response.text

    return ""

def get_nachnamen_teil_html(teil: str) -> str:
    """Nutzt den Spezial-Endpoint des Backends für Nachnamen-Teilstrings."""
    url = f"{BACKEND_URL}/nachnamen/{teil}"
    response = requests.get(url, timeout=10, verify=BACKEND_VERIFY)
    
    if response.status_code == HTTP_OK:
        return response.text

    return ""