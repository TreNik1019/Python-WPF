"""PatientGetRouter mit HTML-Rueckgabe."""

from typing import Annotated, Final

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from loguru import logger

from patient.repository import Pageable
from patient.router.constants import ETAG, IF_NONE_MATCH, IF_NONE_MATCH_MIN_LEN
from patient.router.dependencies import get_service
from patient.service import NotFoundError, PatientDTO, PatientService

__all__ = ["patient_router"]


patient_router: Final = APIRouter(tags=["Lesen"])


@patient_router.get("/{patient_id}", response_class=HTMLResponse)
def get_by_id(
    patient_id: int,
    request: Request,
    service: Annotated[PatientService, Depends(get_service)],
) -> Response:
    """Suche mit der Patient-ID."""
    logger.debug("patient_id={}", patient_id)

    patient: Final = service.find_by_id(patient_id=patient_id)

    if_none_match: Final = request.headers.get(IF_NONE_MATCH)
    if (
        if_none_match is not None
        and len(if_none_match) >= IF_NONE_MATCH_MIN_LEN
        and if_none_match.startswith('"')
        and if_none_match.endswith('"')
    ):
        version = if_none_match[1:-1]

        try:
            if int(version) == patient.version:
                return Response(status_code=status.HTTP_304_NOT_MODIFIED)
        except ValueError:
            logger.debug("invalid version={}", version)

    if _accepts_json(request):
        return JSONResponse(
            content=jsonable_encoder(patient),
            headers={ETAG: f'"{patient.version}"'},
        )

    return HTMLResponse(
        content=_patient_to_html(patient),
        headers={ETAG: f'"{patient.version}"'},
    )


@patient_router.get("", response_class=HTMLResponse)
def get(
    request: Request,
    service: Annotated[PatientService, Depends(get_service)],
) -> Response:
    """Suche mit Query-Parameter."""
    query_params: Final = request.query_params
    print(f"🔍 BACKEND: Incoming query_params: {dict(query_params)}")
    logger.debug("{}", query_params)

    page: Final = query_params.get("page")
    size: Final = query_params.get("size")
    pageable: Final = Pageable.create(number=page, size=size)

    suchparameter = dict(query_params)
    suchparameter.pop("page", None)
    suchparameter.pop("size", None)
    print(f"🔍 BACKEND: suchparameter dict: {suchparameter}")

    try:
        print(f"🔍 BACKEND: Calling service.find()...")
        patient_slice: Final = service.find(
            suchparameter=suchparameter,
            pageable=pageable,
        )
        print(f"🔍 BACKEND: Found {len(patient_slice.content)} patients")
    except NotFoundError as e:
        print(f"🔍 BACKEND: NotFoundError caught - {e}")
        patient_slice = None

    if _accepts_json(request):
        if patient_slice is None:
            return JSONResponse(
                content={
                    "content": [],
                    "page": {
                        "total_elements": 0,
                        "size": pageable.size,
                        "number": pageable.number,
                    },
                }
            )
        return JSONResponse(
            content={
                "content": jsonable_encoder(patient_slice.content),
                "page": {
                    "total_elements": patient_slice.total_elements,
                    "size": pageable.size,
                    "number": pageable.number,
                },
            }
        )

    if patient_slice is None:
        print(f"🔍 BACKEND: Returning empty HTML table")
        html = _patienten_to_html(())
        print(f"🔍 BACKEND: HTML length: {len(html)}")
        return HTMLResponse(content=html)

    html = _patienten_to_html(patient_slice.content)
    print(f"🔍 BACKEND: Returning HTML with {len(patient_slice.content)} rows, total HTML length: {len(html)}")
    return HTMLResponse(content=html)


@patient_router.get("/nachnamen/{teil}", response_class=HTMLResponse)
def get_nachnamen(
    teil: str,
    service: Annotated[PatientService, Depends(get_service)],
) -> HTMLResponse:
    """Suche Nachnamen zum gegebenen Teilstring."""
    logger.debug("teil={}", teil)

    nachnamen: Final = service.find_nachnamen(teil=teil)
    html = "<ul>" + "".join(f"<li>{nachname}</li>" for nachname in nachnamen) + "</ul>"

    return HTMLResponse(content=html)


def _accepts_json(request: Request) -> bool:
    accept_header: Final = request.headers.get("accept", "")
    return "application/json" in accept_header.lower()


def _patienten_to_html(patienten: tuple[PatientDTO, ...]) -> str:
    rows = "".join(_patient_to_table_row(patient) for patient in patienten)

    return f"""
<table>
    <thead>
        <tr>
            <th>ID</th>
            <th>Nachname</th>
            <th>E-Mail</th>
            <th>Geburtsdatum</th>
            <th>Geschlecht</th>
            <th>Familienstand</th>
            <th>PLZ</th>
            <th>Ort</th>
        </tr>
    </thead>
    <tbody>
        {rows}
    </tbody>
</table>
"""


def _patient_to_table_row(patient: PatientDTO) -> str:
    return f"""
<tr>
    <td>{patient.id}</td>
    <td>{patient.nachname}</td>
    <td>{patient.email}</td>
    <td>{patient.geburtsdatum.isoformat()}</td>
    <td>{patient.geschlecht}</td>
    <td>{patient.familienstand}</td>
    <td>{patient.adresse.plz}</td>
    <td>{patient.adresse.ort}</td>
</tr>
"""


def _patient_to_html(patient: PatientDTO) -> str:
    return f"""
<article>
    <h2>Patient {patient.id}</h2>
    <p><strong>Nachname:</strong> {patient.nachname}</p>
    <p><strong>E-Mail:</strong> {patient.email}</p>
    <p><strong>Geburtsdatum:</strong> {patient.geburtsdatum.isoformat()}</p>
    <p><strong>Geschlecht:</strong> {patient.geschlecht}</p>
    <p><strong>Familienstand:</strong> {patient.familienstand}</p>
    <p><strong>Adresse:</strong> {patient.adresse.plz} {patient.adresse.ort}</p>
</article>
"""
