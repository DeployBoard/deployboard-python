from urllib.parse import urlparse

from flask import request, url_for


def test_web_root_redirect_to_dashboard_logged_in(client):
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 302
    assert urlparse(response.location).path == url_for("dashboard_page.dashboard")


def test_web_before_request_logged_in_expired_session(client):
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 0
    response = client.get("/dashboard/", follow_redirects=False)
    assert response.status_code == 302
    assert urlparse(response.location).path == url_for("logout_page.logout")


def test_web_before_request_no_session_redirect_to_login(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 302
    assert urlparse(response.location).path == url_for("login_page.login")


def test_web_before_request_static(client):
    response = client.get("/static/images/rocket-transparent-256px.png")
    assert response.status_code == 200
    assert request.path == "/static/images/rocket-transparent-256px.png"


def test_web_before_request_favicon(client):
    response = client.get("/static/images/favicon.ico")
    assert response.status_code == 200
    assert request.path == "/static/images/favicon.ico"


def test_web_root_settings_redirect(client):
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
    response = client.get("/settings", follow_redirects=False)
    assert response.status_code == 302
    assert urlparse(response.location).path == url_for("users_page.users")


def test_web_root_settings_trailing_slash_redirect(client):
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
    response = client.get("/settings/", follow_redirects=False)
    assert response.status_code == 302
    assert urlparse(response.location).path == url_for("users_page.users")


def test_web_root_inject_theme_light(client):
    with client.session_transaction() as session:
        session["theme"] = "light"
    response = client.get("/login/", follow_redirects=False)
    assert response.status_code == 200
    assert b"light" in response.data


def test_web_root_inject_theme_dark(client):
    with client.session_transaction() as session:
        session["theme"] = "dark"
    response = client.get("/login/", follow_redirects=False)
    assert response.status_code == 200
    assert b"dark" in response.data


def test_web_root_inject_theme_invalid(client):
    with client.session_transaction() as session:
        session["theme"] = "invalid_theme"
    response = client.get("/login/", follow_redirects=False)
    assert response.status_code == 200
    assert b"light" in response.data
