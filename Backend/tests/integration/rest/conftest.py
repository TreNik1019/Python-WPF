"""Fixture fuer pytest: MockDB-App pruefen."""

from common_test import check_readiness
from pytest import fixture

session_scope = "session"


@fixture(scope=session_scope, autouse=True)
def check_readiness_per_session() -> None:
    """Prueft, ob der Appserver erreichbar ist."""
    check_readiness()
    print("Appserver ist ready")
