from unittest.mock import patch

import pytest
from fastapi import HTTPException

from api.util.password_policy import (
    check_length,
    check_lowercase,
    check_number,
    check_password_policy,
    check_special,
    check_uppercase,
)

valid_password = "3xDu&x@oP!xYp9"
account = "Example"


@patch("api.util.password_policy.get_account")
def test_password_policy_string_valid(mock):
    mock.return_value = {
        "account": "Example",
        "password_policy": {
            "length": 1,
            "lowercase": 1,
            "uppercase": 1,
            "number": 1,
            "special": 1,
        },
    }
    response = check_password_policy(account, valid_password)
    assert response["summary"] is True
    assert response["status"] == {
        "length": True,
        "lowercase": True,
        "uppercase": True,
        "number": True,
        "special": True,
    }


@patch("api.util.password_policy.get_account")
def test_password_policy_string_invalid_length(mock):
    mock.return_value = {
        "account": "Example",
        "password_policy": {
            "length": 99,
            "lowercase": 1,
            "uppercase": 1,
            "number": 1,
            "special": 1,
        },
    }
    with pytest.raises(HTTPException):
        response = check_password_policy(account, valid_password)
        assert type(response) is HTTPException
        assert response.status_code == 400
        assert "Password does not meet the policy:" in response.json()["detail"]


@patch("api.util.password_policy.get_account")
def test_password_policy_string_invalid_lowercase(mock):
    mock.return_value = {
        "account": "Example",
        "password_policy": {
            "length": 1,
            "lowercase": 99,
            "uppercase": 1,
            "number": 1,
            "special": 1,
        },
    }
    with pytest.raises(HTTPException):
        response = check_password_policy(account, valid_password)
        assert type(response) is HTTPException
        assert response.status_code == 400
        assert "Password does not meet the policy:" in response.json()["detail"]


@patch("api.util.password_policy.get_account")
def test_password_policy_string_invalid_uppercase(mock):
    mock.return_value = {
        "account": "Example",
        "password_policy": {
            "length": 1,
            "lowercase": 1,
            "uppercase": 99,
            "number": 1,
            "special": 1,
        },
    }
    with pytest.raises(HTTPException):
        response = check_password_policy(account, valid_password)
        assert type(response) is HTTPException
        assert response.status_code == 400
        assert "Password does not meet the policy:" in response.json()["detail"]


@patch("api.util.password_policy.get_account")
def test_password_policy_string_invalid_number(mock):
    mock.return_value = {
        "account": "Example",
        "password_policy": {
            "length": 1,
            "lowercase": 1,
            "uppercase": 1,
            "number": 99,
            "special": 1,
        },
    }
    with pytest.raises(HTTPException):
        response = check_password_policy(account, valid_password)
        assert type(response) is HTTPException
        assert response.status_code == 400
        assert "Password does not meet the policy:" in response.json()["detail"]


@patch("api.util.password_policy.get_account")
def test_password_policy_string_invalid_special(mock):
    mock.return_value = {
        "account": "Example",
        "password_policy": {
            "length": 1,
            "lowercase": 1,
            "uppercase": 1,
            "number": 1,
            "special": 99,
        },
    }
    with pytest.raises(HTTPException):
        response = check_password_policy(account, valid_password)
        assert type(response) is HTTPException
        assert response.status_code == 400
        assert "Password does not meet the policy:" in response.json()["detail"]


def test_password_policy_check_length_success():
    response = check_length(valid_password, 12)
    assert response is True


def test_password_policy_check_length_fail():
    response = check_length("test", 12)
    assert response is False


def test_password_policy_check_lowercase_success():
    response = check_lowercase(valid_password, 1)
    assert response is True


def test_password_policy_check_lowercase_fail():
    response = check_lowercase("TEST", 1)
    assert response is False


def test_password_policy_check_lowercase_fail_count():
    response = check_lowercase(valid_password, 99)
    assert response is False


def test_password_policy_check_uppercase_success():
    response = check_uppercase(valid_password, 1)
    assert response is True


def test_password_policy_check_uppercase_fail():
    response = check_uppercase("test", 1)
    assert response is False


def test_password_policy_check_uppercase_fail_count():
    response = check_uppercase(valid_password, 99)
    assert response is False


def test_password_policy_check_number_success():
    response = check_number(valid_password, 1)
    assert response is True


def test_password_policy_check_number_fail():
    response = check_number("test", 1)
    assert response is False


def test_password_policy_check_number_fail_count():
    response = check_number(valid_password, 99)
    assert response is False


def test_password_policy_check_special_success():
    response = check_special(valid_password, 1)
    assert response is True


def test_password_policy_check_special_fail():
    response = check_special("test", 1)
    assert response is False


def test_password_policy_check_special_fail_count():
    response = check_special(valid_password, 99)
    assert response is False
