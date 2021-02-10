import pytest
from fastapi.testclient import TestClient
from api.main import app
from unittest.mock import patch

client = TestClient(app)


# POST /environments/
def test_post_environments_valid(admin_token):
    body = {'environments': ["Production", "Test", "Dev"]}
    response = client.post(f"/environments/", headers={"Authorization": admin_token}, json=body)
    assert response.status_code == 200
    assert response.json() == {"detail": "Environments updated successfully."}


def test_post_environments_bad_token():
    body = {'environments': ["Production", "Test", "Dev"]}
    response = client.post(f"/environments/", headers={"Authorization": "bad-token"}, json=body)
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_post_environments_invalid_role_viewer(viewer_token):
    body = {'environments': ["Production", "Test", "Dev"]}
    response = client.post(f"/environments/", headers={"Authorization": viewer_token}, json=body)
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


def test_post_environments_invalid_role_editor(editor_token):
    body = {'environments': ["Production", "Test", "Dev"]}
    response = client.post(f"/environments/", headers={"Authorization": editor_token}, json=body)
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


def test_post_environments_invalid_body(admin_token):
    body = []
    response = client.post("/environments/", headers={"Authorization": admin_token}, json=body)
    assert response.status_code == 422


@pytest.mark.skip(reason="The Mock is not triggering the exception.")
@patch("db.mongo.db.accounts")
def test_post_environments_exception(mock_db, admin_token):
    body = {'environments': ["Production", "Test", "Dev"]}
    mock_db.side_effect = Exception('ConnectionFailure')
    response = client.post("/environments/", headers={"Authorization": admin_token}, json=body)
    assert response.status_code == 500
    assert response.json() == {"detail": "Unexpected error occurred."}
    assert mock_db.called_once()
