from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_login():
    response = client.post("/token/", {'username': 'admin@example.com', 'password': 'secret'})
    assert response.status_code == 200
    assert type(response.json()) == dict


def test_invalid_login():
    response = client.post("/token/", {'username': 'admin@example.com', 'password': 'incorrect_password'})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid username or password"}
