import pytest
from fastapi.testclient import TestClient
from api.main import app

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


# TODO: Mock the mongodb exception in the try:expect
# def test_create_apikey_mongo_exception(admin_token):
#     with patch('foo.call_api', side_effect=Exception('mocked error')):
#         with pytest.raises(Exception) as excinfo:
#         #     create_key('localhost:8080', 'spam', 'eggs')
#         assert excinfo.value.message == 'mocked error'
