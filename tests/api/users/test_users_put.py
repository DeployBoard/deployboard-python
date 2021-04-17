from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


# PUT /users/
def test_create_user_valid_user(admin_token):
    body = {"email": "jdoe999@example.com", "role": "Editor", "password": "secret"}
    put_response = client.put(
        "/users/", headers={"Authorization": admin_token}, json=body
    )
    assert put_response.status_code == 200
    assert "_id" in put_response.json()
    get_response = client.get(
        f"/users/{put_response.json()['_id']}", headers={"Authorization": admin_token}
    )
    assert get_response.status_code == 200
    assert "_id" in get_response.json()
    assert "schema_version" in get_response.json()
    assert "email" in get_response.json()
    assert "role" in get_response.json()
    assert "first_name" in get_response.json()
    assert "last_name" in get_response.json()
    assert "enabled" in get_response.json()
    assert "account" in get_response.json()


def test_create_user_existing_user(admin_token):
    body = {"email": "viewer@example.com", "role": "Editor", "password": "secret"}
    response = client.put("/users/", headers={"Authorization": admin_token}, json=body)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "User already exists, may be associated with another account."
    }


def test_create_user_empty_body(admin_token):
    body = {}
    response = client.put("/users/", headers={"Authorization": admin_token}, json=body)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "email"]
    assert response.json()["detail"][0]["msg"] == "field required"
    assert response.json()["detail"][0]["type"] == "value_error.missing"
    assert response.json()["detail"][1]["loc"] == ["body", "role"]
    assert response.json()["detail"][1]["msg"] == "field required"
    assert response.json()["detail"][1]["type"] == "value_error.missing"


def test_create_user_invalid_body_missing_role(admin_token):
    body = {"email": "test@example.com", "password": "secret"}
    response = client.put("/users/", headers={"Authorization": admin_token}, json=body)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "role"]
    assert response.json()["detail"][0]["msg"] == "field required"
    assert response.json()["detail"][0]["type"] == "value_error.missing"


def test_create_user_invalid_body_missing_email(admin_token):
    body = {"role": "Viewer", "password": "secret"}
    response = client.put("/users/", headers={"Authorization": admin_token}, json=body)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "email"]
    assert response.json()["detail"][0]["msg"] == "field required"
    assert response.json()["detail"][0]["type"] == "value_error.missing"


def test_create_user_invalid_body_missing_password(admin_token):
    body = {"email": "test@example.com", "role": "Viewer"}
    response = client.put("/users/", headers={"Authorization": admin_token}, json=body)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "password"]
    assert response.json()["detail"][0]["msg"] == "field required"
    assert response.json()["detail"][0]["type"] == "value_error.missing"


def test_create_user_bad_token():
    response = client.put("/users/", headers={"Authorization": "bad-token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_create_user_invalid_role(viewer_token, seed_data):
    body = {"email": "viewer@example.com", "role": "Editor", "password": "secret"}
    response = client.put("/users/", headers={"Authorization": viewer_token}, json=body)
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}
