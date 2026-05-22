"""HTTP client for retrieving patient data from the FastAPI backend."""

import requests

BACKEND_URL = "http://127.0.0.1:8000/rest"


def get_all(
    nachname: str = "",
    email: str = "",
    page: int = 0,
    size: int = 5,
) -> dict:
    """Fetch patient data from the FastAPI backend.

    Args:
        nachname: Optional last-name filter.
        email: Optional email filter.
        page: Zero-based page number.
        size: Page size.

    Returns:
        The parsed JSON response from the backend.

    Raises:
        RuntimeError: If the backend does not return HTTP 200.
    """
    params = {
        "page": page,
        "size": size,
    }
    if nachname:
        params["nachname"] = nachname
    if email:
        params["email"] = email

    response = requests.get(BACKEND_URL, params=params, timeout=10)
    if response.status_code != 200:
        raise RuntimeError(
            f"FastAPI backend request failed with status code {response.status_code}: "
            f"{response.text}"
        )

    return response.json()
