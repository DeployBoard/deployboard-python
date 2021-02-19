import pytest
from unittest.mock import patch
from src.web.webroutes.dashboard import get_api


# TODO: This test could be better.
@patch('webroutes.dashboard.get_api')
def test_web_dashboard_get_success(mock, client, admin_token):
    mock.return_value.json.return_value = [
        {
            "schema_version": 1,
            "service": "Api",
            "application": "Admin",
            "account": "Example",
            "tags": [
                "python"
            ],
            "versions": [
                {
                    "environment": "Prod",
                    "status": "Deployed",
                    "version": "1.2.0",
                    "timestamp": 1608623640,
                    "custom": {
                        "module": "foo",
                        "color": "green"
                    }
                }
            ],
            "_id": "602ec3a41d6ef526c9362d42"
        }
    ]
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['exp'] = 999999999999999
        session['token'] = admin_token
    response = client.get('/dashboard/')
    assert response.status_code == 200
    assert b'Dashboard' in response.data


@patch('webroutes.dashboard.get_api', side_effect=Exception('mocked error'))
def test_dashboard_get_services_exception(mock, client, admin_token):
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['exp'] = 999999999999999
        session['token'] = admin_token
    response = client.get('/dashboard/')
    assert response.status_code == 500
    assert b'mocked error' in response.data


@patch('requests.get')
def test_dashboard_get_api_success(mock, admin_token):
    mock.return_value.status_code = 200
    mock.return_value.json.return_value = []
    response = get_api('services', admin_token)
    assert response == []


@patch('requests.get', side_effect=Exception('mocked error'))
def test_dashboard_get_api_exception(mock, admin_token):
    with pytest.raises(Exception) as excinfo:
        get_api('services', admin_token)
    assert str(excinfo.value) == 'mocked error'
