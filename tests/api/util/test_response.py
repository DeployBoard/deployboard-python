import pytest
from fastapi import HTTPException
from api.util.response import check_response


def test_check_response_valid():
    current_user = {'account': 'test'}
    data = {'account': 'test', '_id': '0000'}
    response = check_response(current_user, data)
    assert response == data
    assert 'hashed_password' not in response


def test_check_response_contains_hashed_password_as_key():
    current_user = {'account': 'test'}
    data = {'account': 'test', '_id': '0000', 'hashed_password': 'foo'}
    with pytest.raises(HTTPException):
        response = check_response(current_user, data)
        assert response.status_code == 500
        assert response.json['detail'] == 'Unexpected error occurred.'
        assert 'hashed_password' not in response.json()
        assert '_id' not in response.json()


def test_check_response_contains_hashed_password_as_value():
    # If a protected keyword is a value, that's fine. For example if someone named an application 'hashed_password'.
    current_user = {'account': 'hashed_password'}
    data = {'account': 'hashed_password', '_id': '0000'}
    response = check_response(current_user, data)
    assert response == data
    assert 'hashed_password' not in response


def test_check_response_contains_salt_as_key():
    current_user = {'account': 'test'}
    data = {'account': 'test', '_id': '0000', 'salt': 'foo'}
    with pytest.raises(HTTPException):
        response = check_response(current_user, data)
        assert response.status_code == 500
        assert response.json['detail'] == 'Unexpected error occurred.'
        assert 'salt' not in response.json()
        assert '_id' not in response.json()


def test_check_response_contains_salt_as_value():
    # If a protected keyword is a value, that's fine. For example if someone named an application 'salt'.
    current_user = {'account': 'salt'}
    data = {'account': 'salt', '_id': '0000'}
    response = check_response(current_user, data)
    assert response == data
    assert 'salt' not in response


def test_check_response_different_accounts():
    current_user = {'account': 'test'}
    data = {'account': 'diff_account', '_id': '0000'}
    with pytest.raises(HTTPException):
        response = check_response(current_user, data)
        assert response.status_code == 500
        assert response.json['detail'] == 'Unexpected error occurred.'
        assert '_id' not in response.json()
