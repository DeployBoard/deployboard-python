from unittest.mock import patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from api.main import app
from api.routes.services import get_one_service

client = TestClient(app)


# GET /services/{_id}
def test_get_service_valid_admin(admin_token, service):
    response = client.get(
        f"/services/{service}", headers={"Authorization": admin_token}
    )
    assert response.status_code == 200
    assert type(response.json()) == dict


def test_get_service_valid_editor(editor_token, service):
    response = client.get(
        f"/services/{service}", headers={"Authorization": editor_token}
    )
    assert response.status_code == 200
    assert type(response.json()) == dict


def test_get_service_valid_viewer(viewer_token, service):
    response = client.get(
        f"/services/{service}", headers={"Authorization": viewer_token}
    )
    assert response.status_code == 200
    assert type(response.json()) == dict


def test_get_service_bad_token(service):
    response = client.get(
        f"/services/{service}", headers={"Authorization": "bad-token"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.asyncio
@patch("api.routes.services.db")
async def test_get_service_mock_response_none(mock, service):
    user = {
        "account": "Example",
        "name": "pytestuser",
        "role": "Admin",
        "email": "pytestuser@example.com",
    }
    mock.services.find_one.return_value = None
    with pytest.raises(HTTPException):
        response = await get_one_service(service, user)
        # TODO: This test covers the exception, but does not enforce these assertions.
        assert type(response) is HTTPException
        assert response.status_code == 404
        assert response.json()["detail"] == f"{service} not found."


@pytest.mark.asyncio
@patch("api.routes.services.db")
async def test_get_service_mock_response_no_id(mock, service):
    user = {
        "account": "Example",
        "name": "pytestuser",
        "role": "Admin",
        "email": "pytestuser@example.com",
    }
    mock.services.find_one.return_value = {"test": "missing_id"}
    with pytest.raises(HTTPException):
        response = await get_one_service(service, user)
        # TODO: This test covers the exception, but does not enforce these assertions.
        assert type(response) is HTTPException
        assert response.status_code == 404
        assert response.json()["detail"] == f"{service} not found."


@pytest.mark.asyncio
@patch("api.routes.services.db")
async def test_get_service_exception(mock, service):
    user = {
        "account": "Example",
        "name": "pytestuser",
        "role": "Admin",
        "email": "pytestuser@example.com",
    }
    mock.services.find_one.side_effect = Exception("mock")
    with pytest.raises(HTTPException):
        response = await get_one_service(service, user)
        # TODO: This test covers the exception, but does not enforce these assertions.
        assert type(response) is HTTPException
        assert response.status_code == 500
        assert response.json()["detail"] == "Unexpected error occurred. mock"
