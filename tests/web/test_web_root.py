from datetime import datetime, timedelta
from flask import request, url_for


def test_root_no_redirect(client):
    response = client.get('/')
    assert response.status_code == 302
    assert request.path == '/'


def test_root_redirect_to_login(client):
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert request.path == url_for('login_page.login')
    assert b'Email Address' in response.data
    assert b'Password' in response.data
    assert b'Login' in response.data


# def test_root_missing_exp_redirect_to_login(client):
#     with client.session_transaction(subdomain='blue') as session:
#         session['logged_in'] = True
#     response = client.get('/', follow_redirects=True)
#     assert response.status_code == 200
#     assert request.path == url_for('login_page.login')
#     assert b'Email Address' in response.data
#     assert b'Password' in response.data
#     assert b'Login' in response.data
#
# # TODO: Create an Authorized Client as a fixture and pass that in.
# def test_root_redirect_to_dashboard(client):
#     response = client.get('/', follow_redirects=True)
#     assert response.status_code == 200
#     assert request.path == url_for('dashboard_page.dashboard')
#     assert b'Dashboard' in response.data
