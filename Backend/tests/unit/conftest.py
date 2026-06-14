"""Fixtures fuer Unit-Tests mit MockRepository."""

from pytest import fixture

from patient.repository.patient_mock_repository import PatientMockRepository
from patient.service import PatientService


@fixture
def patient_repository() -> PatientMockRepository:
    """Fixture fuer PatientMockRepository."""
    return PatientMockRepository()


@fixture
def patient_service(patient_repository: PatientMockRepository) -> PatientService:
    """Fixture fuer PatientService."""
    return PatientService(patient_repository)
