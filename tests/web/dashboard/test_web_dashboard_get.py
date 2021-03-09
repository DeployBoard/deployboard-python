from unittest.mock import patch


@patch('requests.get')
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
    assert b'Admin' in response.data


@patch('requests.get', side_effect=Exception('mocked error'))
def test_dashboard_get_services_exception(mock, client, admin_token):
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['exp'] = 999999999999999
        session['token'] = admin_token
    response = client.get('/dashboard/')
    assert response.status_code == 200
    assert b'mocked error' in response.data
