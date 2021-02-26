from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_get_me_success(admin_token):
    response = client.get("/me/", headers={"Authorization": admin_token})
    assert response.status_code == 200
    assert type(response.json()) == dict


def test_get_me_no_header():
    response = client.get("/me/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_me_invalid_token():
    response = client.get("/me/", headers={"Authorization": "abcd"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
