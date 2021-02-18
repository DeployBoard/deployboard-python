import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


# GET /services/
def test_get_services_valid_admin(admin_token):
    response = client.get("/services/", headers={"Authorization": admin_token})
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_services_valid_editor(editor_token):
    response = client.get("/services/", headers={"Authorization": editor_token})
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_services_valid_viewer(viewer_token):
    response = client.get("/services/", headers={"Authorization": viewer_token})
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_services_bad_token():
    response = client.get("/services/", headers={"Authorization": "bad-token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
