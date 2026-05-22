"""HTTP client for retrieving patient data from the FastAPI backend."""

import requests
from django.conf import settings

# Read backend URL from Django settings to make it configurable.
BACKEND_URL = getattr(settings, "BACKEND_URL", "http://127.0.0.1:8000/rest")
HTTP_OK = 200


def get_all(
    nachname: str = "",
    email: str = "",
    page: int = 0,
    size: int = 5,
) -> dict[str, object]:
    """Fetch patient data from the FastAPI backend.

    Args:
        nachname: Optional last name filter.
        email: Optional email filter.
        page: Zero-based page number.
        size: Page size.

    Returns:
        The parsed JSON response from the backend.

    Raises:
        RuntimeError: If the backend response is not HTTP 200.

    """
    params: dict[str, str | int] = {"page": page, "size": size}
    if nachname:
        params["nachname"] = nachname
    if email:
        params["email"] = email

    response = requests.get(BACKEND_URL, params=params, timeout=10)
    if response.status_code != HTTP_OK:
        raise RuntimeError(
            f"FastAPI backend request failed with status code {response.status_code}: "
            f"{response.text}"
        )

    return response.json()
