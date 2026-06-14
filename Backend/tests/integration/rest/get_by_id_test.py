# ruff: noqa: S101, D103
"""Tests fuer GET mit Pfadparameter fuer die ID."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, rest_url
from httpx import get
from pytest import mark


@mark.rest
@mark.get_request
@mark.parametrize("patient_id", [1, 20, 30, 50])
def test_get_by_id(patient_id: int) -> None:
    response: Final = get(f"{rest_url}/{patient_id}", verify=ctx)

    assert response.status_code == HTTPStatus.OK
    assert "text/html" in response.headers["content-type"]
    assert f"Patient {patient_id}" in response.text


@mark.rest
@mark.get_request
@mark.parametrize("patient_id", [0, 999999])
def test_get_by_id_not_found(patient_id: int) -> None:
    response: Final = get(f"{rest_url}/{patient_id}", verify=ctx)

    assert response.status_code == HTTPStatus.NOT_FOUND


@mark.rest
@mark.get_request
@mark.parametrize("patient_id,if_none_match", [(20, '"0"'), (30, '"0"')])
def test_get_by_id_etag(patient_id: int, if_none_match: str) -> None:
    headers = {"If-None-Match": if_none_match}

    response: Final = get(
        f"{rest_url}/{patient_id}",
        headers=headers,
        verify=ctx,
    )

    assert response.status_code == HTTPStatus.NOT_MODIFIED
    assert not response.text


@mark.rest
@mark.get_request
@mark.parametrize("patient_id,if_none_match", [(30, "xxx"), (1, 'xxx"')])
def test_get_by_id_etag_invalid(patient_id: int, if_none_match: str) -> None:
    headers = {"If-None-Match": if_none_match}

    response: Final = get(
        f"{rest_url}/{patient_id}",
        headers=headers,
        verify=ctx,
    )

    assert response.status_code == HTTPStatus.OK
    assert f"Patient {patient_id}" in response.text
