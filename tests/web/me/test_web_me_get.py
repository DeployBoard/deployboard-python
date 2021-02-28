from unittest.mock import patch


@patch('requests.get')
def test_web_me_get_success(mock, client, admin_token):
    mock.return_value.json.return_value = {"theme": "Dark"}
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['exp'] = 999999999999999
        session['token'] = admin_token
    response = client.get('/me/')
    assert response.status_code == 200
    assert b'Me' in response.data
    assert b'Dark' in response.data


@patch('requests.get', side_effect=Exception('mocked error'))
def test_web_me_get_exception(mock, client, admin_token):
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['exp'] = 999999999999999
        session['token'] = admin_token
    response = client.get('/me/')
    assert response.status_code == 200
    assert b'mocked error' in response.data
