def test_web_ci_get_success(client, admin_token):
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['exp'] = 999999999999999
        session['token'] = admin_token
    response = client.get('/ci/')
    assert response.status_code == 200
    assert b'ci' in response.data
