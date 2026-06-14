# ruff: noqa: S101, D103
"""Unit-Tests fuer find() und find_nachnamen() von PatientService."""

from pytest import mark, raises

from patient.repository import Pageable
from patient.service import NotFoundError, PatientService

ANZAHL_PATIENTEN = 4


@mark.unit
@mark.unit_find
def test_find_all(patient_service: PatientService) -> None:
    pageable = Pageable(size=10, number=0)

    patienten_slice = patient_service.find(suchparameter={}, pageable=pageable)

    assert len(patienten_slice.content) == ANZAHL_PATIENTEN
    assert patienten_slice.total_elements == ANZAHL_PATIENTEN


@mark.unit
@mark.unit_find
@mark.parametrize("nachname", ["Alpha", "Beta", "Gamma", "Delta"])
def test_find_by_nachname(patient_service: PatientService, nachname: str) -> None:
    suchparameter = {"nachname": nachname}
    pageable = Pageable(size=5, number=0)

    patienten_slice = patient_service.find(
        suchparameter=suchparameter,
        pageable=pageable,
    )

    assert len(patienten_slice.content) == 1
    assert patienten_slice.content[0].nachname == nachname


@mark.unit
@mark.unit_find
def test_find_by_nachname_not_found(patient_service: PatientService) -> None:
    nachname = "Notfound"
    suchparameter = {"nachname": nachname}
    pageable = Pageable(size=5, number=0)

    with raises(NotFoundError) as err:
        patient_service.find(suchparameter=suchparameter, pageable=pageable)

    assert err.type == NotFoundError
    assert err.value.suchparameter is not None
    assert err.value.suchparameter.get("nachname") == nachname


@mark.unit
@mark.unit_find
@mark.parametrize("email", ["alpha@acme.de", "beta@acme.de"])
def test_find_by_email(patient_service: PatientService, email: str) -> None:
    suchparameter = {"email": email}
    pageable = Pageable(size=5, number=0)

    patienten_slice = patient_service.find(
        suchparameter=suchparameter,
        pageable=pageable,
    )

    assert len(patienten_slice.content) == 1
    assert patienten_slice.content[0].email == email


@mark.unit
@mark.unit_find
def test_find_by_email_not_found(patient_service: PatientService) -> None:
    email = "not@found.mock"
    suchparameter = {"email": email}
    pageable = Pageable(size=5, number=0)

    with raises(NotFoundError) as err:
        patient_service.find(suchparameter=suchparameter, pageable=pageable)

    assert err.type == NotFoundError
    assert err.value.suchparameter is not None
    assert err.value.suchparameter.get("email") == email


@mark.unit
@mark.unit_find
@mark.parametrize("teil", ["a", "A", "Al"])
def test_find_nachnamen(patient_service: PatientService, teil: str) -> None:
    nachnamen = patient_service.find_nachnamen(teil=teil)

    assert len(nachnamen) > 0
    assert all(teil.lower() in nachname.lower() for nachname in nachnamen)


@mark.unit
@mark.unit_find
def test_find_nachnamen_not_found(patient_service: PatientService) -> None:
    with raises(NotFoundError):
        patient_service.find_nachnamen(teil="xxx")
