from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


# POST /deploy/
def test_post_deploy_valid_request(admin_apikey):
    # Should create a new service.
    body = {
        "application": "PyTestDeployAppNewApp",
        "service": "PyTestDeployServiceNewService",
        "environment": "PyTestNewEnv",
        "status": "Deploying",
        "version": "v1.0.0"
    }
    post_response = client.post("/deploy/", headers={"X-API-Key": admin_apikey}, json=body)
    # TODO: make a query to make sure the object created properly in db.
    # TODO: make sure the new environment was created in the accounts collection.
    # TODO: make sure the log got inserted into the logs table.
    assert post_response.status_code == 200
    assert post_response.json() == {'status': 'ok'}


def test_post_deploy_valid_request_2(admin_apikey):
    # Should update the existing service from previous test.
    body = {
        "application": "PyTestDeployAppNewApp",
        "service": "PyTestDeployServiceNewService",
        "environment": "PyTestNewEnv",
        "status": "Deployed",
        "version": "v1.0.0"
    }
    post_response = client.post("/deploy/", headers={"X-API-Key": admin_apikey}, json=body)
    # TODO: make a query to make sure the object updated properly in db.
    assert post_response.status_code == 200
    assert post_response.json() == {'status': 'ok'}


def test_post_deploy_valid_request_3(admin_apikey):
    # Should update the existing service from previous test with the new version and status.
    body = {
        "application": "PyTestDeployAppNewApp",
        "service": "PyTestDeployServiceNewService",
        "environment": "PyTestNewEnv",
        "status": "Deploying",
        "version": "v2.0.0"
    }
    post_response = client.post("/deploy/", headers={"X-API-Key": admin_apikey}, json=body)
    # TODO: make a query to make sure the object updated properly in db.
    assert post_response.status_code == 200
    assert post_response.json() == {'status': 'ok'}


def test_post_deploy_empty_body(admin_apikey):
    body = {}
    response = client.post("/deploy/", headers={"X-API-Key": admin_apikey}, json=body)
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "field required"
    assert response.json()['detail'][0]['type'] == "value_error.missing"


def test_post_deploy_bad_apikey():
    body = {
        "application": "SampleApp",
        "service": "SampleService",
        "environment": "Prod",
        "status": "Deploying",
        "version": "v1.0.2",
        "custom": {
            "module": "example-module",
            "user": "JohnDoe"
        }
    }
    response = client.post("/deploy/", headers={"X-API-Key": "000000000000000000000bad"}, json=body)
    assert response.status_code == 403
    assert response.json() == {"detail": "Could not validate credentials."}


def test_post_deploy_invalid_role(viewer_apikey):
    body = {
        "application": "SampleApp",
        "service": "SampleService",
        "environment": "Prod",
        "status": "Deploying",
        "version": "v1.0.2",
        "custom": {
            "module": "example-module",
            "user": "JohnDoe"
        }
    }
    response = client.post("/deploy/", headers={"X-API-Key": viewer_apikey}, json=body)
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}
