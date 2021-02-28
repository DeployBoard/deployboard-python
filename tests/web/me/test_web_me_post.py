from flask import url_for
from urllib.parse import urlparse
from unittest.mock import patch


@patch('requests.post')
def test_web_me_post_success(mock, client, admin_token):
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['exp'] = 999999999999999
        session['token'] = admin_token
    response = client.post('/me/', data=dict(
        first_name='pytest',
        last_name='pytest',
        avatar='pytest',
        theme='pytest',
        csrf='pytest'
    ), follow_redirects=False)
    assert response.status_code == 302
    assert urlparse(response.location).path == url_for('me_page.me')


@patch('requests.post', side_effect=Exception('mocked error'))
def test_web_me_post_exception(mock, client, admin_token):
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['exp'] = 999999999999999
        session['token'] = admin_token
    response = client.post('/me/', data=dict(
        first_name='pytest',
        last_name='pytest',
        avatar='pytest',
        theme='pytest',
        csrf='pytest'
    ), follow_redirects=False)
    assert response.status_code == 200
    assert b'mocked error' in response.data
