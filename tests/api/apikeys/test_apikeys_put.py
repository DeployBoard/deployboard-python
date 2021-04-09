import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from unittest.mock import patch
from api.main import app
from api.routes.apikeys import create_apikey
from api.models.apikeys import CreateApiKey

client = TestClient(app)


# POST /apikeys/
def test_create_apikey_valid_apikey(admin_token):
    body = {
        "name": "pytest-success",
        "role": "Editor"
    }
    put_response = client.put("/apikeys/", headers={"Authorization": admin_token}, json=body)
    assert put_response.status_code == 200
    assert '_id' in put_response.json()
    get_response = client.get(f"/apikeys/{put_response.json()['_id']}", headers={"Authorization": admin_token})
    assert get_response.status_code == 200
    assert '_id' in get_response.json()
    assert 'schema_version' in get_response.json()
    assert 'account' in get_response.json()
    assert 'name' in get_response.json()
    assert 'role' in get_response.json()
    assert 'created_by' in get_response.json()
    assert 'created_timestamp' in get_response.json()
    assert 'modified_by' in get_response.json()
    assert 'modified_timestamp' in get_response.json()


def test_create_apikey_empty_apikey(admin_token):
    body = {}
    response = client.put("/apikeys/", headers={"Authorization": admin_token}, json=body)
    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ["body", "name"]
    assert response.json()['detail'][0]['msg'] == "field required"
    assert response.json()['detail'][0]['type'] == "value_error.missing"
    assert response.json()['detail'][1]['loc'] == ["body", "role"]
    assert response.json()['detail'][1]['msg'] == "field required"
    assert response.json()['detail'][1]['type'] == "value_error.missing"


def test_create_apikey_invalid_body_missing_role(admin_token):
    body = {"name": "failed-test"}
    response = client.put("/apikeys/", headers={"Authorization": admin_token}, json=body)
    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ["body", "role"]
    assert response.json()['detail'][0]['msg'] == "field required"
    assert response.json()['detail'][0]['type'] == "value_error.missing"


def test_create_apikey_invalid_body_missing_name(admin_token):
    body = {"role": "Viewer"}
    response = client.put("/apikeys/", headers={"Authorization": admin_token}, json=body)
    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ["body", "name"]
    assert response.json()['detail'][0]['msg'] == "field required"
    assert response.json()['detail'][0]['type'] == "value_error.missing"


def test_create_apikey_bad_token():
    response = client.put("/apikeys/", headers={"Authorization": "bad-token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_create_apikey_invalid_role(viewer_token):
    body = {
        "name": "failed-test",
        "role": "Editor"
    }
    response = client.put("/apikeys/", headers={"Authorization": viewer_token}, json=body)
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


@pytest.mark.asyncio
@patch('api.routes.apikeys.db')
async def test_create_apikey_exception(mock):
    body = CreateApiKey(name="pytest-exception", role="Editor")
    user = {
        "account": "Example",
        "name": "pytestuser",
        "role": "Admin",
        "email": "pytestuser@example.com"
    }
    mock.apikeys.insert_one.side_effect = Exception('mock')
    with pytest.raises(HTTPException):
        response = await create_apikey(body, user)
        # TODO: This test covers the exception, but does not enforce these assertions.
        assert type(response) is HTTPException
        assert response.status_code == 500
        assert response.json()['detail'] == "Unexpected error occurred. mock"
