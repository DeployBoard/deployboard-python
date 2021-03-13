import pytest
from unittest.mock import patch
from webutil.webapi import webapi


@patch('webutil.webapi.request')
def test_web_api_get_success(mock, admin_token):
    mock.return_value.status_code = 200
    mock.return_value.json.return_value = []
    response = webapi('get', 'services/', token=admin_token)
    assert response == []


@patch('webutil.webapi.request')
def test_web_api_get_non_200(mock, admin_token):
    mock.return_value.status_code = 404
    mock.return_value.json.return_value = {'detail': 'mock response'}
    with pytest.raises(Exception) as excinfo:
        webapi('get', 'services/', token=admin_token)
    assert str(excinfo.value) == "(404, {'detail': 'mock response'})"


@patch('webutil.webapi.request', side_effect=Exception('mocked error'))
def test_web_api_get_exception(mock, admin_token):
    with pytest.raises(Exception) as excinfo:
        webapi('get', 'services/', token=admin_token)
    assert str(excinfo.value) == 'mocked error'
