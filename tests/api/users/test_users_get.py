import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


# GET /users/
def test_get_users(admin_token):
    response = client.get("/users/", headers={"Authorization": admin_token})
    assert response.status_code == 200
    # TODO: Can we assert == model?
    assert type(response.json()) == list
    assert 'hashed_password' not in response.json()[0]


def test_get_users_bad_token():
    response = client.get("/users/", headers={"Authorization": "bad-token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_users_invalid_role(viewer_token):
    response = client.get("/users/", headers={"Authorization": viewer_token})
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}
