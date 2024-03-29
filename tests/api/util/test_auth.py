from unittest.mock import patch

import pytest
from fastapi.exceptions import HTTPException

from api.util.auth import (
    authenticate_user,
    generate_password_hash,
    get_api_key_in_header,
    verify_api_key,
    verify_password,
)


def test_authenticate_user_valid():
    email = "admin@example.com"
    response = authenticate_user(email, "secret")
    assert response is not None
    assert type(response) == dict
    assert response["email"] == email


def test_authenticate_user_invalid_password():
    response = authenticate_user("admin@example.com", "password")
    assert response is False


def test_authenticate_user_invalid_user():
    response = authenticate_user("invaliduser@example.com", "password")
    assert response is False


def test_authenticate_user_disabled_user():
    response = authenticate_user("disabledadmin@example.com", "secret")
    assert response is False


def test_verify_password_success():
    password = "secret"
    hash_password = (
        "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # secret
    )
    response = verify_password(password, hash_password)
    assert response is True


def test_verify_password_failure():
    password = "invalidpassword"
    hash_password = (
        "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # secret
    )
    response = verify_password(password, hash_password)
    assert response is False


def test_generate_password_hash():
    response = generate_password_hash("testpassword", "testsalt")
    assert response is not None
    assert type(response) == str


def test_api_key_in_header():
    response = get_api_key_in_header("X-API-Key:pytest")
    assert response is not None
    assert type(response) == str
    assert response == "X-API-Key:pytest"


def test_verify_api_key_success(apikey):
    response = verify_api_key(apikey)
    assert response is not None
    assert type(response) == dict
    assert "_id" in response
    assert "role" in response


def test_verify_api_key_invalid():
    with pytest.raises(HTTPException) as excinfo:
        verify_api_key("551137c2f9e1fac808a5f572")
    assert excinfo.type == HTTPException
    assert excinfo.value.status_code == 403
    assert excinfo.value.detail == "Could not validate credentials."


@patch("api.util.auth.db")
def test_verify_api_key_exception(mock, apikey):
    mock.apikeys.find_one.side_effect = Exception("mock")
    with pytest.raises(HTTPException) as excinfo:
        verify_api_key(apikey)
        assert type(excinfo) == HTTPException
        assert excinfo.value.status_code == 500
        assert excinfo.value.detail == "Unexpected error occurred."
