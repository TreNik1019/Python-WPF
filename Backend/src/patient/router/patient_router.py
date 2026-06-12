"""PatientGetRouter."""

from dataclasses import asdict
from typing import Annotated, Any, Final

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import JSONResponse
from loguru import logger

from patient.repository import Pageable
from patient.repository.slice import Slice
from patient.router.constants import ETAG, IF_NONE_MATCH, IF_NONE_MATCH_MIN_LEN
from patient.router.dependencies import get_service
from patient.router.page import Page
from patient.service import PatientDTO, PatientService

__all__ = ["patient_router"]


patient_router: Final = APIRouter(tags=["Lesen"])


@patient_router.get("/{patient_id}")
def get_by_id(
    patient_id: int,
    request: Request,
    service: Annotated[PatientService, Depends(get_service)],
) -> Response:
    """Suche mit der Patient-ID."""
    logger.debug("patient_id={}", patient_id)

    patient: Final = service.find_by_id(patient_id=patient_id)
    logger.debug("{}", patient)

    if_none_match: Final = request.headers.get(IF_NONE_MATCH)
    if (
        if_none_match is not None
        and len(if_none_match) >= IF_NONE_MATCH_MIN_LEN
        and if_none_match.startswith('"')
        and if_none_match.endswith('"')
    ):
        version = if_none_match[1:-1]
        logger.debug("version={}", version)

        try:
            if int(version) == patient.version:
                return Response(status_code=status.HTTP_304_NOT_MODIFIED)
        except ValueError:
            logger.debug("invalid version={}", version)

    return JSONResponse(
        content=_patient_to_dict(patient),
        headers={ETAG: f'"{patient.version}"'},
    )


@patient_router.get("")
def get(
    request: Request,
    service: Annotated[PatientService, Depends(get_service)],
) -> JSONResponse:
    """Suche mit Query-Parameter."""
    query_params: Final = request.query_params
    logger.debug("{}", query_params)

    page: Final = query_params.get("page")
    size: Final = query_params.get("size")
    pageable: Final = Pageable.create(number=page, size=size)

    suchparameter = dict(query_params)
    suchparameter.pop("page", None)
    suchparameter.pop("size", None)

    patient_slice: Final = service.find(
        suchparameter=suchparameter,
        pageable=pageable,
    )

    result: Final = _patient_slice_to_page(patient_slice, pageable)
    logger.debug("{}", result)

    return JSONResponse(content=result)


@patient_router.get("/nachnamen/{teil}")
def get_nachnamen(
    teil: str,
    service: Annotated[PatientService, Depends(get_service)],
) -> JSONResponse:
    """Suche Nachnamen zum gegebenen Teilstring."""
    logger.debug("teil={}", teil)

    nachnamen: Final = service.find_nachnamen(teil=teil)
    return JSONResponse(content=nachnamen)


def _patient_slice_to_page(
    patient_slice: Slice[PatientDTO],
    pageable: Pageable,
) -> dict[str, Any]:
    patient_dict: Final = tuple(
        _patient_to_dict(patient) for patient in patient_slice.content
    )

    page: Final = Page.create(
        content=patient_dict,
        pageable=pageable,
        total_elements=patient_slice.total_elements,
    )

    return asdict(obj=page)


def _patient_to_dict(patient: PatientDTO) -> dict[str, Any]:
    patient_dict: Final = asdict(obj=patient)
    patient_dict.pop("version")
    patient_dict.update({"geburtsdatum": patient.geburtsdatum.isoformat()})

    return patient_dict
