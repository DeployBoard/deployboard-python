import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


# GET /users/{_id}
def test_get_user_valid_user(admin_token, user):
    response = client.get(f"/users/{user}", headers={"Authorization": admin_token})
    assert response.status_code == 200
    assert response.json()["_id"] == user
    assert "hashed_password" not in response.json()
    assert "_id" in response.json()


def test_get_user_bad_token(user):
    response = client.get(f"/users/{user}", headers={"Authorization": "bad-token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_user_invalid_role(viewer_token, user):
    response = client.get(f"/users/{user}", headers={"Authorization": viewer_token})
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


def test_get_user_missing_user(admin_token):
    response = client.get(
        "/users/000000000000000000000000", headers={"Authorization": admin_token}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found."}


@pytest.mark.skip(reason="TODO: This is temporary, fix this test")
def test_get_user_invalid_userid(admin_token):
    response = client.get("/users/foo", headers={"Authorization": admin_token})
    assert response.status_code == 400
    assert response.json() == {
        "detail": (
            "'foo' is not a valid ObjectId, it must be a 12-byte input"
            "or a24-character hex string"
        )
    }
