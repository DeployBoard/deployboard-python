import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


# POST /services/
def test_create_service_valid(admin_token):
    body = {
        "application": "Test",
        "service": "Pytest"
    }
    put_response = client.put("/services/", headers={"Authorization": admin_token}, json=body)
    assert put_response.status_code == 200
    assert '_id' in put_response.json()
    get_response = client.get(f"/services/{put_response.json()['_id']}", headers={"Authorization": admin_token})
    assert get_response.status_code == 200
    assert '_id' in get_response.json()
    assert 'schema_version' in get_response.json()
    assert 'account' in get_response.json()
    assert 'application' in get_response.json()
    assert 'service' in get_response.json()


def test_create_service_empty_body(admin_token):
    body = {}
    response = client.put("/services/", headers={"Authorization": admin_token}, json=body)
    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ["body", "service"]
    assert response.json()['detail'][0]['msg'] == "field required"
    assert response.json()['detail'][0]['type'] == "value_error.missing"
    assert response.json()['detail'][1]['loc'] == ["body", "application"]
    assert response.json()['detail'][1]['msg'] == "field required"
    assert response.json()['detail'][1]['type'] == "value_error.missing"


def test_create_service_invalid_body_missing_application(admin_token):
    body = {"service": "failed-test"}
    response = client.put("/services/", headers={"Authorization": admin_token}, json=body)
    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ["body", "application"]
    assert response.json()['detail'][0]['msg'] == "field required"
    assert response.json()['detail'][0]['type'] == "value_error.missing"


def test_create_service_invalid_body_missing_service(admin_token):
    body = {"application": "failed-test"}
    response = client.put("/services/", headers={"Authorization": admin_token}, json=body)
    assert response.status_code == 422
    assert response.json()['detail'][0]['loc'] == ["body", "service"]
    assert response.json()['detail'][0]['msg'] == "field required"
    assert response.json()['detail'][0]['type'] == "value_error.missing"


def test_create_service_bad_token():
    response = client.put("/services/", headers={"Authorization": "bad-token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_create_service_invalid_role(viewer_token):
    body = {
        "application": "TestViewer",
        "service": "PytestViewer"
    }
    response = client.put("/services/", headers={"Authorization": viewer_token}, json=body)
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


@patch('routes.services.db')
def test_create_service_exists(mock, admin_token):
    body = {
        "application": "TestExists",
        "service": "PytestExists"
    }
    mock.return_value = body
    response = client.put("/services/", headers={"Authorization": admin_token}, json=body)
    assert response.status_code == 400
    assert response.json() == {"detail": "Service already exists in this account."}


# TODO: Mock the mongodb exception in the try:expect
@pytest.mark.skip(reason="Not using the second call of db. Maybe refactor the source to 2 separate functions.")
@patch('routes.services.db', side_effect=[None, Exception("mocked error")])
def test_create_service_mongo_exception(mock, admin_token):
    body = {
        "application": "Test348579",
        "service": "Pytest2908345809"
    }
    response = client.put("/services/", headers={"Authorization": admin_token}, json=body)
    assert response.status_code == 500
    assert response.json() == {"detail": "Unexpected error occurred."}
