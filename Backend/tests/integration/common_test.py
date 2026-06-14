# ruff: noqa: S101, D103
"""Allgemeine Daten fuer die Tests."""

from http import HTTPStatus
from pathlib import Path
from ssl import create_default_context
from typing import Any, Final

from httpx import get

__all__ = [
    "base_url",
    "ctx",
    "health_url",
    "rest_path",
    "rest_url",
    "timeout",
]

schema: Final = "https"
port: Final = 8000
host: Final = "127.0.0.1"

base_url: Final = f"{schema}://{host}:{port}"
rest_path: Final = "/rest"
rest_url: Final = f"{base_url}{rest_path}"
health_url: Final = f"{base_url}/health"
timeout: Final = 2

certificate: Final = str(Path("tests") / "integration" / "certificate.crt")
ctx = create_default_context(cafile=certificate)


def check_readiness() -> None:
    """Prueft, ob der Appserver bereit ist."""
    response: Final = get(
        f"{health_url}/readiness",
        verify=ctx,
        timeout=timeout,
    )

    if response.status_code != HTTPStatus.OK:
        raise RuntimeError(f"readiness mit Statuscode {response.status_code}")

    response_body: Final = response.json()

    if not isinstance(response_body, dict):
        raise RuntimeError("readiness ohne Dictionary im Response-Body")

    status: Final[Any | None] = response_body.get("db")

    if status != "up":
        raise RuntimeError(f"readiness mit Meldungstext {status}")
