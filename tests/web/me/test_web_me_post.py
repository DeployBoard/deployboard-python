from unittest.mock import patch
from urllib.parse import urlparse

from flask import url_for


@patch("webroutes.me.webapi")
def test_web_me_post_success(mock, client, admin_token):
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.post(
        "/me/",
        data=dict(
            first_name="pytest",
            last_name="pytest",
            avatar="pytest",
            theme="pytest",
            csrf="pytest",
        ),
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert urlparse(response.location).path == url_for("me_page.me")


@patch("webroutes.me.webapi", side_effect=Exception("mock"))
def test_web_me_post_exception(mock, client, admin_token):
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.post(
        "/me/",
        data=dict(
            first_name="pytest",
            last_name="pytest",
            avatar="pytest",
            theme="pytest",
            csrf="pytest",
        ),
        follow_redirects=False,
    )
    assert response.status_code == 200
    assert b"mock" in response.data
