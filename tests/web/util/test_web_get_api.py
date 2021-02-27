import pytest
from unittest.mock import patch
from webutil.webapi import get_api


@patch('requests.get')
def test_web_get_api_success(mock, admin_token):
    mock.return_value.status_code = 200
    mock.return_value.json.return_value = []
    response = get_api('services', admin_token)
    assert response == []


@patch('requests.get', side_effect=Exception('mocked error'))
def test_web_get_api_exception(mock, admin_token):
    with pytest.raises(Exception) as excinfo:
        get_api('services', admin_token)
    assert str(excinfo.value) == 'mocked error'
