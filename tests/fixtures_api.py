import pytest
from fastapi.testclient import TestClient
from api.main import app
from scripts.db_seed import seed

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def seed_data():
    return seed()


@pytest.fixture(scope="session")
def admin_token():
    response = client.post("/token/", data={'username': 'admin@example.com', 'password': 'secret'})
    token = response.json()['access_token']
    return f'Bearer {token}'


@pytest.fixture(scope="session")
def editor_token():
    response = client.post("/token/", data={'username': 'editor@example.com', 'password': 'secret'})
    token = response.json()['access_token']
    return f'Bearer {token}'


@pytest.fixture(scope="session")
def viewer_token():
    response = client.post("/token/", data={'username': 'viewer@example.com', 'password': 'secret'})
    token = response.json()['access_token']
    return f'Bearer {token}'


@pytest.fixture(scope="session")
def user(admin_token):
    body = {
        "email": "pytestuser@example.com",
        "role": "Viewer",
        "password": "secret"
    }
    response = client.put("/users/", headers={"Authorization": admin_token}, json=body)
    resp = response.json()
    return resp['_id']

@pytest.fixture(scope="session")
def apikey(admin_token):
    body = {
        "name": "pytest-api-key-to-delete",
        "role": "Editor"
    }
    response = client.put("/apikeys/", headers={"Authorization": admin_token}, json=body)
    resp = response.json()
    return resp['_id']


@pytest.fixture(scope="session")
def admin_apikey(admin_token):
    body = {
        "name": "pytest-admin-api-key",
        "role": "Admin"
    }
    response = client.put("/apikeys/", headers={"Authorization": admin_token}, json=body)
    resp = response.json()
    return resp['_id']


@pytest.fixture(scope="session")
def editor_apikey(admin_token):
    body = {
        "name": "pytest-editor-api-key",
        "role": "Editor"
    }
    response = client.put("/apikeys/", headers={"Authorization": admin_token}, json=body)
    resp = response.json()
    return resp['_id']


@pytest.fixture(scope="session")
def viewer_apikey(admin_token):
    body = {
        "name": "pytest-viewer-api-key",
        "role": "Viewer"
    }
    response = client.put("/apikeys/", headers={"Authorization": admin_token}, json=body)
    resp = response.json()
    return resp['_id']


@pytest.fixture(scope="session")
def service(admin_token):
    body = {
        "application": "Test",
        "service": "Fixture"
    }
    response = client.put("/services/", headers={"Authorization": admin_token}, json=body)
    resp = response.json()
    return resp['_id']
