"""HTTP client for retrieving patient data from the FastAPI backend."""

import requests
from django.conf import settings

# Read backend URL from Django settings to make it configurable.
BACKEND_URL = getattr(settings, "BACKEND_URL", "https://127.0.0.1:8000/rest")
BACKEND_VERIFY = getattr(settings, "BACKEND_VERIFY", False)
HTTP_OK = 200


def get_all(
    nachname: str = "",
    email: str = "",
    page: int = 0,
    size: int = 5,
) -> str:
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

    print(f"🔎 FRONTEND SERVICE: Sending GET to {BACKEND_URL} with params: {params}")
    response = requests.get(
        BACKEND_URL,
        params=params,
        timeout=10,
        verify=BACKEND_VERIFY,
    )
    print(f"🔎 FRONTEND SERVICE: Response status: {response.status_code}")
    if response.status_code != HTTP_OK:
        print(f"🔎 FRONTEND SERVICE: ERROR response text: {response.text[:500]}")
        raise RuntimeError(
            f"FastAPI backend request failed with status code {response.status_code}: "
            f"{response.text}"
        )

    return response.text
