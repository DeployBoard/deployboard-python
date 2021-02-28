import pytest
from unittest.mock import patch
from webutil.webapi import post_api


@patch('requests.post')
def test_web_post_api_success(mock, admin_token):
    mock.return_value.status_code = 200
    mock.return_value.json.return_value = []
    data = {}
    response = post_api('me/', admin_token, data)
    assert response == []


@patch('requests.post', side_effect=Exception('mocked error'))
def test_web_post_api_exception(mock, admin_token):
    data = {}
    with pytest.raises(Exception) as excinfo:
        post_api('me/', admin_token, data)
    assert str(excinfo.value) == 'mocked error'
