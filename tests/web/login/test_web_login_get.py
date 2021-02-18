from datetime import datetime, timedelta
from flask import request, url_for
from urllib.parse import urlparse
from unittest.mock import patch


def test_web_login_get_success(client):
    response = client.get('/login/')
    assert response.status_code == 200
    assert request.path == url_for('login_page.login')
    assert b'Email' in response.data
    assert b'Password' in response.data


def test_web_login_get_logged_in(client):
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['exp'] = 999999999999999
    response = client.get('/login/', follow_redirects=False)
    assert response.status_code == 302
    assert urlparse(response.location).path == url_for('dashboard_page.dashboard')


def test_web_login_get_no_trailing_slash(client):
    response = client.get('/login', follow_redirects=False)
    assert response.status_code == 308
    assert urlparse(response.location).path == url_for('login_page.login')
