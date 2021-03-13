import pytest
from unittest.mock import patch


@patch('webroutes.apikeys.webapi')
def test_web_apikeys_get_success(mock, client, admin_token):
    mock.return_value = [
        {
            "_id": "5fe51081e178d1bda551cc2a",
            "schema_version": 1,
            "account": "Example",
            "name": "test-api-key",
            "role": "Editor",
            "enabled": True,
            "created_by": "jdoe@example.com",
            "created_timestamp": 1610053395,
            "modified_by": "admin@example.com",
            "modified_timestamp": 1610921529
        }
    ]
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['exp'] = 999999999999999
        session['token'] = admin_token
    response = client.get('/settings/apikeys/')
    assert response.status_code == 200
    assert b'test-api-key' in response.data
    assert b'Created By' in response.data


@patch('webroutes.apikeys.webapi', side_effect=Exception('mock'))
def test_web_apikeys_get_exception(mock, client, admin_token):
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['exp'] = 999999999999999
        session['token'] = admin_token
    response = client.get('/settings/apikeys/')
    assert response.status_code == 200
    assert b'mock' in response.data
