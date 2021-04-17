from unittest.mock import patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from api.main import app
from api.routes.logs import get_one_log

client = TestClient(app)


# GET /logs/{_id}
def test_get_log_valid_key(admin_token, seed_data):
    response = client.get(
        f"/logs/{str(seed_data['logs'][0])}", headers={"Authorization": admin_token}
    )
    assert response.status_code == 200
    assert response.json()["_id"] == str(seed_data["logs"][0])
    assert "hashed_password" not in response.json()
    assert "_id" in response.json()


def test_get_log_bad_token(seed_data):
    response = client.get(
        f"/logs/{str(seed_data['logs'][0])}", headers={"Authorization": "bad-token"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.skip(
    reason="Currently all roles are able to view logs, so none are invalid."
)
def test_get_log_invalid_role(viewer_token, seed_data):
    response = client.get(
        f"/logs/{str(seed_data['logs'][0])}", headers={"Authorization": viewer_token}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


def test_get_log_missing_key(admin_token):
    log_id = "000000000000000000000000"
    response = client.get(f"/logs/{log_id}", headers={"Authorization": admin_token})
    assert response.status_code == 404
    assert response.json() == {"detail": f"Log: {log_id} not found"}


@pytest.mark.skip(reason="TODO: This is temporary, fix this test")
def test_get_log_invalid_log_id(admin_token):
    response = client.get("/log/foo", headers={"Authorization": admin_token})
    assert response.status_code == 400
    assert response.json() == {
        "detail": (
            "'foo' is not a valid ObjectId, it must be a 12-byte input"
            "or a24-character hex string"
        )
    }


@pytest.mark.asyncio
@patch("api.routes.logs.db")
async def test_get_log_exception(mock):
    user = {
        "account": "Example",
        "name": "pytestuser",
        "role": "Admin",
        "email": "pytestuser@example.com",
    }
    mock.logs.find_one.side_effect = Exception("mock")
    with pytest.raises(HTTPException):
        response = await get_one_log("000000000000000000000000", user)
        # TODO: This test covers the exception, but does not enforce these assertions.
        assert type(response) is HTTPException
        assert response.status_code == 500
        assert response.json()["detail"] == "Unexpected error occurred. mock"
