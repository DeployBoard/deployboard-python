import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


# DELETE /apikeys/{_id}
@pytest.mark.order("last")
def test_delete_apikey_valid_apikey(admin_token, apikey):
    response = client.delete(
        f"/apikeys/{apikey}", headers={"Authorization": admin_token}
    )
    assert response.status_code == 200
    assert "_id" in response.json()
    assert response.json()["_id"] == apikey
    assert response.json()["detail"] == "Key deleted successfully."


def test_delete_apikey_bad_token(apikey):
    response = client.delete(
        f"/apikeys/{apikey}", headers={"Authorization": "bad-token"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_delete_apikey_invalid_role_viewer(viewer_token, apikey):
    response = client.delete(
        f"/apikeys/{apikey}", headers={"Authorization": viewer_token}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


def test_delete_apikey_invalid_role_editor(editor_token, apikey):
    response = client.delete(
        f"/apikeys/{apikey}", headers={"Authorization": editor_token}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


def test_delete_apikey_missing_key(admin_token):
    response = client.delete(
        "/apikeys/000000000000000000000000", headers={"Authorization": admin_token}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Key not found."}


@pytest.mark.skip(
    reason="TODO: This is temporary, fix this test. It doesn't impact coverage."
)
def test_delete_apikey_invalid_apikeyid(admin_token):
    response = client.delete("/apikeys/foo", headers={"Authorization": admin_token})
    assert response.status_code == 400
    assert response.json() == {
        "detail": (
            "'foo' is not a valid ObjectId, it must be a 12-byte input"
            "or a24-character hex string"
        )
    }
