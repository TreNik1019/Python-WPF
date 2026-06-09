"""MainApp fuer GET-Endpunkte mit MockDB."""

from collections.abc import Awaitable, Callable
from pathlib import Path
from time import time
from typing import Final

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import FileResponse
from loguru import logger
from prometheus_fastapi_instrumentator import Instrumentator

from patient.banner import banner
from patient.problem_details import create_problem_details
from patient.router import health_router, patient_router
from patient.service import ForbiddenError, NotFoundError

__all__ = [
    "forbidden_error_handler",
    "not_found_error_handler",
]


app: Final = FastAPI()

banner(app.routes)

Instrumentator().instrument(app).expose(app)


@app.middleware("http")
async def log_request_header(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Request loggen."""
    logger.debug("{} '{}'", request.method, request.url)
    return await call_next(request)


@app.middleware("http")
async def log_response_time(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Antwortzeit loggen."""
    start = time()
    response = await call_next(request)
    duration_ms = (time() - start) * 1000

    logger.debug(
        "Response time: {:.2f} ms, statuscode: {}",
        duration_ms,
        response.status_code,
    )

    return response


app.include_router(patient_router, prefix="/rest")
app.include_router(health_router, prefix="/health")


@app.get("/favicon.ico")
def favicon() -> FileResponse:
    """favicon.ico ermitteln."""
    src_path: Final = Path("src")
    file_name: Final = "favicon.ico"
    favicon_path: Final = Path("patient") / "static" / file_name
    file_path: Final = src_path / favicon_path if src_path.is_dir() else favicon_path

    logger.debug("file_path={}", file_path)

    return FileResponse(
        path=file_path,
        headers={"Content-Disposition": f"attachment; filename={file_name}"},
    )


@app.exception_handler(NotFoundError)
def not_found_error_handler(_request: Request, _err: NotFoundError) -> Response:
    """Errorhandler fuer NotFoundError."""
    return create_problem_details(status_code=status.HTTP_404_NOT_FOUND)


@app.exception_handler(ForbiddenError)
def forbidden_error_handler(_request: Request, _err: ForbiddenError) -> Response:
    """Errorhandler fuer ForbiddenError."""
    return create_problem_details(status_code=status.HTTP_403_FORBIDDEN)
