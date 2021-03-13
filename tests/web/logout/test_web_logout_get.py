from flask import url_for
from urllib.parse import urlparse


def test_web_logout_get_logged_in(client):
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['exp'] = 999999999999999
    response = client.get('/logout/', follow_redirects=False)
    assert response.status_code == 302
    assert urlparse(response.location).path == url_for('login_page.login')


def test_web_logout_get_not_logged_in(client):
    response = client.get('/logout/', follow_redirects=False)
    assert response.status_code == 302
    assert urlparse(response.location).path == url_for('login_page.login')


def test_web_logout_get_no_trailing_slash(client):
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['exp'] = 999999999999999
    response = client.get('/logout', follow_redirects=False)
    assert response.status_code == 308
    assert urlparse(response.location).path == url_for('logout_page.logout')
