"""HealthRouter."""

from typing import Any, Final

from fastapi import APIRouter

__all__ = ["router"]

router: Final = APIRouter(tags=["Health"])


@router.get("/liveness")
def liveness() -> dict[str, Any]:
    """Liveness-Prüfung."""
    return {"status": "up"}


@router.get("/readiness")
def readiness() -> dict[str, Any]:
    """Readiness-Prüfung."""
    return {"status": "up"}
