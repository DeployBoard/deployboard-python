import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from api.main import app
from unittest.mock import patch
from api.routes.environments import get_environments

client = TestClient(app)


# GET /environments/
def test_get_environments_admin(admin_token):
    response = client.get("/environments/", headers={"Authorization": admin_token})
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_environments_editor(editor_token):
    response = client.get("/environments/", headers={"Authorization": editor_token})
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_environments_viewer(viewer_token):
    response = client.get("/environments/", headers={"Authorization": viewer_token})
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_environments_bad_token():
    response = client.get("/environments/", headers={"Authorization": "bad-token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.asyncio
@patch('api.routes.environments.db')
async def test_get_environments_exception(mock):
    user = {
        "account": "Example",
        "name": "pytestuser",
        "role": "Admin",
        "email": "pytestuser@example.com"
    }
    mock.accounts.find_one.side_effect = Exception('mock')
    with pytest.raises(HTTPException):
        response = await get_environments(user)
        # TODO: This test covers the exception, but does not enforce these assertions.
        assert type(response) is HTTPException
        assert response.status_code == 500
        assert response.json()['detail'] == "Unexpected error occurred. mock"
