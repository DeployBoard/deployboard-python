import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


# GET /logs/{_id}
def test_get_log_valid_key(admin_token, log):
    response = client.get(f"/logs/{log}", headers={"Authorization": admin_token})
    assert response.status_code == 200
    assert response.json()['_id'] == log
    assert 'hashed_password' not in response.json()
    assert '_id' in response.json()


def test_get_log_bad_token(apikey):
    response = client.get(f"/logs/{apikey}", headers={"Authorization": "bad-token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_log_invalid_role(viewer_token, log):
    response = client.get(f"/logs/{log}", headers={"Authorization": viewer_token})
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


def test_get_log_missing_key(admin_token):
    log_id = '000000000000000000000000'
    response = client.get(f"/logs/{log_id}", headers={"Authorization": admin_token})
    assert response.status_code == 404
    assert response.json() == {"detail": f"Log: {log_id} not found"}


@pytest.mark.skip(reason="TODO: This is temporary, fix this test")
def test_get_log_invalid_log_id(admin_token):
    response = client.get("/log/foo", headers={"Authorization": admin_token})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "'foo' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string"
    }
