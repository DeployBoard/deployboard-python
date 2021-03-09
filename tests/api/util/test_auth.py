import pytest
from api.util.auth import authenticate_user, verify_password, get_password_hash, get_api_key_in_header, verify_api_key
from fastapi.exceptions import HTTPException

def test_authenticate_user_valid():
    email = 'admin@example.com'
    response = authenticate_user(email, 'secret')
    assert response is not None
    assert type(response) == dict
    assert response['email'] == email


def test_authenticate_user_invalid_password():
    response = authenticate_user('admin@example.com', 'password')
    assert response is False


def test_authenticate_user_invalid_user():
    response = authenticate_user('invaliduser@example.com', 'password')
    assert response is False


def test_authenticate_user_disabled_user():
    response = authenticate_user('disabledadmin@example.com', 'secret')
    assert response is False


def test_verify_password_success():
    password = 'secret'
    hash_password = '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW'  # secret
    response = verify_password(password, hash_password)
    assert response is True


def test_verify_password_failure():
    password = 'invalidpassword'
    hash_password = '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW'  # secret
    response = verify_password(password, hash_password)
    assert response is False


def test_get_password_hash():
    response = get_password_hash('testpassword')
    assert response is not None
    assert type(response) == str


def test_api_key_in_header():
    response = get_api_key_in_header('X-API-Key:pytest')
    assert response is not None
    assert type(response) == str
    assert response is 'X-API-Key:pytest'


def test_verify_api_key_success(apikey):
    response = verify_api_key(apikey)
    assert response is not None
    assert type(response) == dict
    assert '_id' in response
    assert 'role' in response


# TODO: Get this test to work
# def test_verify_api_key_invalid():
#     response = verify_api_key('551137c2f9e1fac808a5f572')
#     assert response is not None
#     assert type(response) == HTTPException
#     assert response.status_code is 403
#     assert response.detail is 'Could not validate credentials.'
#
#
# TODO: Mock Exception
# def test_verify_api_key_exception():
#     response = verify_api_key('551137c2f9e1fac808a5f572')
#     assert response is not None
#     assert type(response) == HTTPException
#     assert response.status_code is 500
#     assert response.detail is 'Unexpected error occurred.'
