from unittest.mock import patch


@patch('requests.get')
def test_web_environments_get_success(mock, client, admin_token):
    mock.return_value.json.return_value = ["Prod, Test, Dev"]
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['exp'] = 999999999999999
        session['token'] = admin_token
    response = client.get('/settings/environments/')
    assert response.status_code == 200
    assert b'Environments' in response.data
    assert b'Prod' in response.data


@patch('requests.get', side_effect=Exception('mocked error'))
def test_web_environments_get_exception(mock, client, admin_token):
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['exp'] = 999999999999999
        session['token'] = admin_token
    response = client.get('/settings/environments/')
    assert response.status_code == 200
    assert b'mocked error' in response.data
