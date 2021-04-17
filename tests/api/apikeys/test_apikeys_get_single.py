import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


# GET /apikeys/{_id}
def test_get_apikey_valid_key(admin_token, apikey):
    response = client.get(f"/apikeys/{apikey}", headers={"Authorization": admin_token})
    assert response.status_code == 200
    assert response.json()["_id"] == apikey
    assert "hashed_password" not in response.json()
    assert "_id" in response.json()


def test_get_apikey_bad_token(apikey):
    response = client.get(f"/apikeys/{apikey}", headers={"Authorization": "bad-token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_apikey_invalid_role(viewer_token, apikey):
    response = client.get(f"/apikeys/{apikey}", headers={"Authorization": viewer_token})
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


def test_get_apikey_missing_key(admin_token):
    response = client.get(
        "/apikeys/000000000000000000000000", headers={"Authorization": admin_token}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Key not found."}


@pytest.mark.skip(reason="TODO: This is temporary, fix this test")
def test_get_apikey_invalid_key_id(admin_token):
    response = client.get("/apikeys/foo", headers={"Authorization": admin_token})
    assert response.status_code == 400
    assert response.json() == {
        "detail": (
            "'foo' is not a valid ObjectId, it must be a 12-byte input"
            "or a24-character hex string"
        )
    }
