import pytest
from fastapi import HTTPException
from unittest.mock import patch
from api.util.account import get_account

valid_account = 'Example'


def test_get_account_valid():
    response = get_account(valid_account)
    assert type(response) is dict
    assert response['account'] == 'Example'
    assert type(response['environments']) == list
    assert type(response['created_timestamp']) == int
    assert type(response['password_policy']) == dict


def test_get_account_missing():
    with pytest.raises(HTTPException):
        response = get_account('missing_account')
        assert type(response) is HTTPException
        assert response.status_code == 400
        assert response.json()['detail'] == "Account not found."


@patch('api.util.account.db')
def test_get_account_missing_mocked(mock):
    mock.accounts.find_one.return_value = None
    with pytest.raises(HTTPException):
        response = get_account('missing_account')
        assert type(response) is HTTPException
        assert response.status_code == 400
        assert response.json()['detail'] == "Account not found."


@patch('api.util.account.db')
def test_get_account_exception(mock):
    mock.accounts.find_one.side_effect = Exception('mock')
    with pytest.raises(HTTPException):
        response = get_account('exception_account')
        assert type(response) is HTTPException
        assert response.status_code == 500
        assert response.json()['detail'] == "Unexpected error occurred: mock"
