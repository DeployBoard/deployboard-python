from unittest.mock import patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from api.main import app
from api.models.environments import UpdateEnvironment
from api.routes.environments import update_environment

client = TestClient(app)


# POST /environments/
def test_post_environments_valid(admin_token):
    body = {"environments": ["Production", "Test", "Dev"]}
    response = client.post(
        "/environments/", headers={"Authorization": admin_token}, json=body
    )
    assert response.status_code == 200
    assert response.json() == {"detail": "Environments updated successfully."}


def test_post_environments_bad_token():
    body = {"environments": ["Production", "Test", "Dev"]}
    response = client.post(
        "/environments/", headers={"Authorization": "bad-token"}, json=body
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_post_environments_invalid_role_viewer(viewer_token):
    body = {"environments": ["Production", "Test", "Dev"]}
    response = client.post(
        "/environments/", headers={"Authorization": viewer_token}, json=body
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


def test_post_environments_invalid_role_editor(editor_token):
    body = {"environments": ["Production", "Test", "Dev"]}
    response = client.post(
        "/environments/", headers={"Authorization": editor_token}, json=body
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


def test_post_environments_invalid_body(admin_token):
    body = []
    response = client.post(
        "/environments/", headers={"Authorization": admin_token}, json=body
    )
    assert response.status_code == 422


@pytest.mark.asyncio
@patch("api.routes.environments.db")
async def test_post_environments_exception(mock):
    body = UpdateEnvironment(environments=["mock"])
    user = {
        "account": "Example",
        "name": "pytestuser",
        "role": "Admin",
        "email": "pytestuser@example.com",
    }
    mock.accounts.update_one.side_effect = Exception("mock")
    with pytest.raises(HTTPException):
        response = await update_environment(body, user)
        # TODO: This test covers the exception, but does not enforce these assertions.
        assert type(response) is HTTPException
        assert response.status_code == 500
        assert response.json()["detail"] == "Unexpected error occurred. mock"
