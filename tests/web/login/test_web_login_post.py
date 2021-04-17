from unittest.mock import patch
from urllib.parse import urlparse

from flask import request, url_for


@patch("jose.jwt.decode")
@patch("webroutes.login.webapi")
def test_web_login_post_success(
    mock_post, mock_decode, client, admin_username, password
):
    mock_post.return_value.status_code = 200
    mock_post.return_value = {"status_code": 200, "access_token": "abc123"}
    mock_decode.return_value = {"sub": "abc", "exp": 999999999999999}
    response = client.post(
        "/login/",
        data=dict(email=admin_username, password=password, csrf="pytest"),
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert urlparse(response.location).path == url_for("dashboard_page.dashboard")


def test_web_login_post_no_email(client, password):
    response = client.post(
        "/login/", data=dict(password=password), follow_redirects=True
    )
    assert response.status_code == 400
    assert request.path == url_for("login_page.login")
    assert b"Bad Request" in response.data


def test_web_login_post_no_password(client, admin_username):
    response = client.post(
        "/login/", data=dict(email=admin_username), follow_redirects=True
    )
    assert response.status_code == 400
    assert request.path == url_for("login_page.login")
    assert b"Bad Request" in response.data


@patch("webroutes.login.webapi", side_effect=Exception("mock"))
def test_web_login_post_exception(mock, client, admin_username, password):
    response = client.post(
        "/login/",
        data=dict(email=admin_username, password=password, csrf="pytest"),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert request.path == url_for("login_page.login")
    assert b"mock" in response.data
