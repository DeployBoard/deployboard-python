import pytest
from api.util.auth import authenticate_user, verify_password, get_password_hash


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
