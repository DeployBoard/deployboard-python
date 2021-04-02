from fastapi.testclient import TestClient
from api.main import app
# from unittest.mock import patch
# from routes.me import update_user_in_db

client = TestClient(app)


def test_update_me_success(viewer_token):
    body = {
        "first_name": "Py",
        "last_name": "Test",
        "theme": "pytest",
        "avatar": "https://pytest",
    }
    patch_response = client.patch("/me/", headers={"Authorization": viewer_token}, json=body)
    assert patch_response.status_code == 200
    assert type(patch_response.json()) == dict
    assert patch_response.json()['modified_count'] == '1'
    get_response = client.get("/me/", headers={"Authorization": viewer_token})
    assert type(get_response.json()) == dict
    assert get_response.json()['first_name'] == 'Py'
    assert get_response.json()['last_name'] == 'Test'
    assert get_response.json()['theme'] == 'pytest'
    assert get_response.json()['avatar'] == 'https://pytest'


def test_update_me_no_header():
    response = client.patch("/me/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_update_me_invalid_token():
    response = client.patch("/me/", headers={"Authorization": "abcd"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_patch_me_no_update(viewer_token):
    body = {}
    patch_response = client.patch("/me/", headers={"Authorization": viewer_token}, json=body)
    assert patch_response.status_code == 200
    assert type(patch_response.json()) == dict
    assert patch_response.json()['modified_count'] == '0'


def test_patch_me_invalid_update(viewer_token):
    body = {
        'role': 'Admin'
    }
    patch_response = client.patch("/me/", headers={"Authorization": viewer_token}, json=body)
    assert patch_response.status_code == 200
    assert type(patch_response.json()) == dict
    assert patch_response.json()['modified_count'] == '0'


# TODO: This is not working.
# @patch("db.mongo.db.users")
# def test_me_update_user_in_db(mock_db):
#     # query = {"_id": ObjectId("_id")}
#     update_command = {"$set": {"first_name": "Py"}}
#     query = {"_id": "6032471da98bf27613af2c38"}
#     mock_db.side_effect = Exception('ConnectionFailure')
#     response = update_user_in_db(query, update_command)
#     assert response.status_code == 500
#     assert response.json() == {"detail": "Unexpected error occurred."}
#     assert mock_db.called_once()
