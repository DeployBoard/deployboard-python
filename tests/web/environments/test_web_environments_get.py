import pytest
from unittest.mock import patch
from webutil.webapi import get_api


@patch('webutil.webapi.get_api')
def test_web_dashboard_get_success(mock, client, admin_token):
    mock.return_value.json.return_value = ["Prod, Test, Dev"]
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['exp'] = 999999999999999
        session['token'] = admin_token
    response = client.get('/dashboard/')
    assert response.status_code == 200
    assert b'Environments' in response.data
    assert b'Prod' in response.data


@patch('webutil.webapi.get_api', side_effect=Exception('mocked error'))
def test_dashboard_get_services_exception(mock, client, admin_token):
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['exp'] = 999999999999999
        session['token'] = admin_token
    response = client.get('/dashboard/')
    assert response.status_code == 500
    assert b'mocked error' in response.data
