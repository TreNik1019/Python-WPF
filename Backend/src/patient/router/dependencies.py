"""Factory-Funktionen für Dependency Injection."""

from typing import Annotated

from fastapi import Depends

from patient.repository.patient_mock_repository import PatientMockRepository
from patient.service.patient_service import PatientService


def get_repository() -> PatientMockRepository:
    """Factory-Funktion für MockRepository."""
    return PatientMockRepository()


def get_service(
    repo: Annotated[PatientMockRepository, Depends(get_repository)],
) -> PatientService:
    """Factory-Funktion für PatientService."""
    return PatientService(repo=repo)
