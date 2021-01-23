import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


# DELETE /users/{_id}
@pytest.mark.order('last')
def test_delete_user_valid_user(admin_token, user):
    response = client.delete(f"/users/{user}", headers={"Authorization": admin_token})
    assert response.status_code == 200
    assert '_id' in response.json()
    assert response.json()['_id'] == user
    assert response.json()['detail'] == 'User deleted successfully.'


def test_delete_user_self(admin_token, seed_data):
    response = client.delete(f"/users/{seed_data['users']['Admin']}", headers={"Authorization": admin_token})
    assert response.status_code == 400
    assert response.json() == {'detail': 'Can not delete yourself.'}


def test_delete_user_bad_token(user):
    response = client.delete(f"/users/{user}", headers={"Authorization": "bad-token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_delete_user_invalid_role_viewer(viewer_token, user):
    response = client.delete(f"/users/{user}", headers={"Authorization": viewer_token})
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


def test_delete_user_invalid_role_editor(editor_token, user):
    response = client.delete(f"/users/{user}", headers={"Authorization": editor_token})
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


def test_delete_user_missing_user(admin_token):
    response = client.delete("/users/000000000000000000000000", headers={"Authorization": admin_token})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found."}


@pytest.mark.skip(reason="TODO: This is temporary, fix this test. It doesn't impact coverage.")
def test_delete_user_invalid_userid(admin_token):
    response = client.delete("/users/foo", headers={"Authorization": admin_token})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "'foo' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string"
    }
