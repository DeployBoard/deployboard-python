import pytest
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
        "application": "Test",
        "service": "Pytest"
    }
    response = client.put("/services/", headers={"Authorization": viewer_token}, json=body)
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


# TODO: Mock the mongodb exception in the try:expect
# def test_create_service_mongo_exception(admin_token):
