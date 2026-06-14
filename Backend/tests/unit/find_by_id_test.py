# ruff: noqa: S101, D103
"""Unit-Tests fuer find_by_id() von PatientService."""

from dataclasses import asdict

from pytest import mark, raises

from patient.service import NotFoundError, PatientDTO, PatientService


@mark.unit
@mark.unit_find_by_id
@mark.parametrize("patient_id", [1, 20, 30, 50])
def test_find_by_id(patient_service: PatientService, patient_id: int) -> None:
    patient_dto = patient_service.find_by_id(patient_id=patient_id)

    assert isinstance(patient_dto, PatientDTO)
    assert patient_dto.id == patient_id
    assert asdict(patient_dto)["id"] == patient_id


@mark.unit
@mark.unit_find_by_id
@mark.parametrize("patient_id", [0, 999999])
def test_find_by_id_not_found(
    patient_service: PatientService,
    patient_id: int,
) -> None:
    with raises(NotFoundError) as err:
        patient_service.find_by_id(patient_id=patient_id)

    assert err.type == NotFoundError
    assert err.value.patient_id == patient_id
