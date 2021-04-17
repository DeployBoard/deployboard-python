import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


# PATCH /users/{_id}
def test_patch_user_valid_user(admin_token, user):
    body = {"first_name": "pytest_user", "password": "secret"}
    response = client.patch(
        f"/users/{user}", headers={"Authorization": admin_token}, json=body
    )
    assert response.status_code == 200
    assert response.json() == {"status": "Updated successfully."}
    assert "hashed_password" not in response.json()
    assert "password" not in response.json()


def test_patch_user_valid_user_no_updates(admin_token, user):
    body = {}
    response = client.patch(
        f"/users/{user}", headers={"Authorization": admin_token}, json=body
    )
    assert response.status_code == 200
    assert response.json() == {"modified_count": "0"}
    assert "hashed_password" not in response.json()
    assert "password" not in response.json()


def test_patch_user_bad_token(user):
    body = {}
    response = client.patch(
        f"/users/{user}", headers={"Authorization": "bad-token"}, json=body
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_patch_user_invalid_role(viewer_token, user):
    body = {}
    response = client.patch(
        f"/users/{user}", headers={"Authorization": viewer_token}, json=body
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


def test_patch_user_missing_user(admin_token):
    body = {"first_name": "bozo"}
    response = client.patch(
        "/users/000000000000000000000099",
        headers={"Authorization": admin_token},
        json=body,
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found."}


@pytest.mark.skip(reason="TODO: This is temporary, fix this test")
def test_patch_user_invalid_userid(admin_token):
    response = client.patch("/users/foo", headers={"Authorization": admin_token})
    assert response.status_code == 400
    assert response.json() == {
        "detail": (
            "'foo' is not a valid ObjectId, it must be a 12-byte input"
            "or a24-character hex string"
        )
    }
