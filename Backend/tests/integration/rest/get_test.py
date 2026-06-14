# ruff: noqa: S101, D103
"""Tests fuer GET mit Query-Parameter."""

from http import HTTPStatus
from typing import Final

from common_test import ctx, rest_url
from httpx import get
from pytest import mark


@mark.rest
@mark.get_request
def test_get_all() -> None:
    response: Final = get(rest_url, verify=ctx)

    assert response.status_code == HTTPStatus.OK
    assert "text/html" in response.headers["content-type"]
    assert "<table>" in response.text
    assert "Alpha" in response.text
    assert "Beta" in response.text
    assert "Gamma" in response.text
    assert "Delta" in response.text


@mark.rest
@mark.get_request
@mark.parametrize("email", ["alpha@acme.de", "beta@acme.de"])
def test_get_by_email(email: str) -> None:
    response: Final = get(rest_url, params={"email": email}, verify=ctx)

    assert response.status_code == HTTPStatus.OK
    assert email in response.text


@mark.rest
@mark.get_request
@mark.parametrize("email", ["nicht@vorhanden.com", "joe.doe@acme.de"])
def test_get_by_email_not_found(email: str) -> None:
    response: Final = get(rest_url, params={"email": email}, verify=ctx)

    assert response.status_code == HTTPStatus.NOT_FOUND


@mark.rest
@mark.get_request
@mark.parametrize("teil", ["Al", "a"])
def test_get_by_nachname(teil: str) -> None:
    response: Final = get(rest_url, params={"nachname": teil}, verify=ctx)

    assert response.status_code == HTTPStatus.OK
    assert "<table>" in response.text


@mark.rest
@mark.get_request
@mark.parametrize("nachname", ["Notfound", "Foo-Bar"])
def test_get_by_nachname_not_found(nachname: str) -> None:
    response: Final = get(rest_url, params={"nachname": nachname}, verify=ctx)

    assert response.status_code == HTTPStatus.NOT_FOUND


@mark.rest
@mark.get_request
@mark.parametrize("teil", ["a", "A"])
def test_get_nachnamen(teil: str) -> None:
    response: Final = get(f"{rest_url}/nachnamen/{teil}", verify=ctx)

    assert response.status_code == HTTPStatus.OK
    assert "text/html" in response.headers["content-type"]
    assert "<ul>" in response.text
    assert "<li>" in response.text


@mark.rest
@mark.get_request
@mark.parametrize("teil", ["xxx", "Abc"])
def test_get_nachnamen_not_found(teil: str) -> None:
    response: Final = get(f"{rest_url}/nachnamen/{teil}", verify=ctx)

    assert response.status_code == HTTPStatus.NOT_FOUND
