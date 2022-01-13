from unittest.mock import patch
from urllib.parse import urlparse

from flask import url_for


@patch("webroutes.apikeys.webapi")
def test_web_apikeys_post_add_success(mock, client, admin_token):
    mock.return_value = {}
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.post(
        "/settings/apikeys/",
        data=dict(
            apikey_name="pytest-api-key",
            apikey_role="Viewer",
            action="add",
            csrf="pytest",
        ),
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert urlparse(response.location).path == url_for("apikeys_page.apikeys")


@patch("webroutes.apikeys.webapi")
def test_web_apikeys_post_edit_success(mock, client, admin_token):
    mock.return_value = {}
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.post(
        "/settings/apikeys/",
        data=dict(
            apikey_id="000000000000000000000000",
            apikey_name="pytest-api-key",
            apikey_role="Viewer",
            apikey_enabled="True",
            action="edit",
            csrf="pytest",
        ),
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert urlparse(response.location).path == url_for("apikeys_page.apikeys")


@patch("webroutes.apikeys.webapi")
def test_web_apikeys_post_delete_success(mock, client, admin_token):
    mock.return_value = {}
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.post(
        "/settings/apikeys/",
        data=dict(apikey_id="000000000000000000000000", action="delete", csrf="pytest"),
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert urlparse(response.location).path == url_for("apikeys_page.apikeys")


@patch("webroutes.apikeys.webapi")
def test_web_apikeys_post_unexpected(mock, client, admin_token):
    mock.return_value = {}
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.post(
        "/settings/apikeys/", data=dict(action="unexpected", csrf="pytest")
    )
    assert response.status_code == 200
    assert b"Unexpected error occurred." in response.data


@patch("webroutes.apikeys.webapi", side_effect=Exception("mock exception"))
def test_web_apikeys_post_exception(mock, client, admin_token):
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.post(
        "/settings/apikeys/",
        data=dict(
            apikey_name="pytest-api-key",
            apikey_role="Viewer",
            action="add",
            csrf="pytest",
        ),
    )
    assert response.status_code == 200
    assert b"mock exception" in response.data
