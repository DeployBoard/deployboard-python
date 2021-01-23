import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


# GET /apikeys/
def test_get_apikeys(admin_token):
    response = client.get("/apikeys/", headers={"Authorization": admin_token})
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_apikeys_bad_token():
    response = client.get("/apikeys/", headers={"Authorization": "bad-token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_apikeys_invalid_role(viewer_token):
    response = client.get("/apikeys/", headers={"Authorization": viewer_token})
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}
