import pytest
from unittest.mock import patch
from src.web.webroutes.applications import get_services


# TODO: This test could be better.
@patch('webroutes.applications.get_services')
def test_web_applications_get_success(mock, client, admin_token):
    mock.return_value.json.return_value = [
        {
            "schema_version": 1,
            "service": "Api",
            "application": "Sample",
            "account": "Example",
            "tags": [
                "python"
            ],
            "versions": [
                {
                    "environment": "Dev",
                    "status": "Deployed",
                    "version": "1.3.0",
                    "timestamp": 1608433640,
                    "custom": {
                        "module": "foo",
                        "color": "green"
                    }
                }
            ],
            "_id": "602ec3a41d6ef526c9362d42"
        },
    ]
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['exp'] = 999999999999999
        session['token'] = admin_token
    response = client.get('/applications/')
    assert response.status_code == 200
    assert b'Applications' in response.data


@patch('requests.get')
def test_web_applications_get_services_success(mock, admin_token):
    mock.return_value.status_code = 200
    mock.return_value.json.return_value = []
    response = get_services(admin_token)
    assert response == []


@patch('requests.get', side_effect=Exception('mocked error'))
def test_web_applications_get_services_exception(mock, admin_token):
    with pytest.raises(Exception) as excinfo:
        get_services(admin_token)
    assert str(excinfo.value) == 'mocked error'
