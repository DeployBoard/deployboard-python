import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


# PATCH /apikeys/{_id}
def test_patch_apikey_valid_apikey(admin_token, apikey):
    body = {"name": "pytest-api-key", "enabled": True}
    response = client.patch(
        f"/apikeys/{apikey}", headers={"Authorization": admin_token}, json=body
    )
    assert response.status_code == 200
    assert response.json() == {"status": "Updated successfully."}


def test_patch_apikey_valid_apikey_no_updates(admin_token, apikey):
    body = {}
    response = client.patch(
        f"/apikeys/{apikey}", headers={"Authorization": admin_token}, json=body
    )
    assert response.status_code == 200
    assert response.json() == {"modified_count": "0"}


def test_patch_apikey_bad_token(apikey):
    body = {}
    response = client.patch(
        f"/apikeys/{apikey}", headers={"Authorization": "bad-token"}, json=body
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_patch_apikey_invalid_role(viewer_token, apikey):
    body = {}
    response = client.patch(
        f"/apikeys/{apikey}", headers={"Authorization": viewer_token}, json=body
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


def test_patch_apikey_missing_apikey(admin_token):
    body = {"name": "bozo"}
    response = client.patch(
        "/apikeys/000000000000000000000099",
        headers={"Authorization": admin_token},
        json=body,
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Key not found."}


@pytest.mark.skip(reason="TODO: This is temporary, fix this test")
def test_patch_apikey_invalid_apikey(admin_token):
    response = client.patch("/apikeys/foo", headers={"Authorization": admin_token})
    assert response.status_code == 400
    assert response.json() == {
        "detail": (
            "'foo' is not a valid ObjectId, it must be a 12-byte input"
            "or a24-character hex string"
        )
    }
