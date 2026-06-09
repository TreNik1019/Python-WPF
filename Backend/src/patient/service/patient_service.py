"""Geschäftslogik zum Lesen von Patientendaten."""

from collections.abc import Mapping, Sequence
from typing import Final

from loguru import logger

from patient.repository import Pageable, Slice
from patient.repository.patient_mock_repository import PatientMockRepository
from patient.service.exceptions import NotFoundError
from patient.service.patient_dto import PatientDTO

__all__ = ["PatientService"]


class PatientService:
    """Service-Klasse mit Geschäftslogik für Patient."""

    def __init__(self, repo: PatientMockRepository) -> None:
        """Konstruktor mit abhängigem MockRepository."""
        self.repo = repo

    def find_by_id(self, patient_id: int) -> PatientDTO:
        """Suche mit der Patient-ID."""
        logger.debug("patient_id={}", patient_id)

        patient = self.repo.find_by_id(patient_id=patient_id)

        if patient is None:
            raise NotFoundError(patient_id=patient_id)

        patient_dto: Final = PatientDTO(patient)
        logger.debug("{}", patient_dto)

        return patient_dto

    def find(
        self,
        suchparameter: Mapping[str, str],
        pageable: Pageable,
    ) -> Slice[PatientDTO]:
        """Suche mit Suchparameter."""
        logger.debug("{}", suchparameter)

        patient_slice: Final = self.repo.find(
            suchparameter=suchparameter,
            pageable=pageable,
        )

        if len(patient_slice.content) == 0:
            raise NotFoundError(suchparameter=suchparameter)

        patienten_dto: Final = tuple(
            PatientDTO(patient) for patient in patient_slice.content
        )

        patienten_dto_slice = Slice(
            content=patienten_dto,
            total_elements=patient_slice.total_elements,
        )

        logger.debug("{}", patienten_dto_slice)

        return patienten_dto_slice

    def find_nachnamen(self, teil: str) -> Sequence[str]:
        """Suche Nachnamen zu einem Teilstring."""
        logger.debug("teil={}", teil)

        nachnamen: Final = self.repo.find_nachnamen(teil=teil)

        if len(nachnamen) == 0:
            raise NotFoundError

        logger.debug("{}", nachnamen)

        return nachnamen
