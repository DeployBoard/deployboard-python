import pytest
from fastapi.testclient import TestClient
from api.main import app
from unittest.mock import patch

client = TestClient(app)


# GET /environments/
def test_get_environments(admin_token):
    response = client.get("/environments/", headers={"Authorization": admin_token})
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_environments_bad_token():
    response = client.get("/environments/", headers={"Authorization": "bad-token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


# @pytest.mark.skip(reason="The Mock is not triggering the exception.")
@patch("db.mongo.db.accounts")
def test_get_environments_exception(mock_db, admin_token):
    mock_db.side_effect = Exception('ConnectionFailure')
    response = client.get("/environments/", headers={"Authorization": admin_token})
    assert response.status_code == 500
    assert response.json() == {"detail": "Unexpected error occurred."}
    assert mock_db.called_once()
