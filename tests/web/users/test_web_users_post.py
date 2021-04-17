from unittest.mock import patch
from urllib.parse import urlparse

from flask import url_for


@patch("webroutes.users.webapi")
def test_web_users_post_add_success(mock, client, admin_token):
    mock.return_value = {}
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.post(
        "/settings/users/",
        data=dict(
            user_email="pytest_viewer@example.com",
            user_role="Viewer",
            user_first_name="PyTestFirstName",
            user_last_name="PyTestLastName",
            user_password="pytestpassword",
            action="add",
            csrf="pytest",
        ),
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert urlparse(response.location).path == url_for("users_page.users")


@patch("webroutes.users.webapi")
def test_web_users_post_edit_success(mock, client, admin_token):
    mock.return_value = {}
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.post(
        "/settings/users/",
        data=dict(
            user_id="000000000000000000000000",
            user_email="pytest_viewer@example.com",
            user_role="Viewer",
            user_enabled="True",
            user_first_name="PyTestFirstName",
            user_last_name="PyTestLastName",
            user_password="pytestpassword",
            action="edit",
            csrf="pytest",
        ),
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert urlparse(response.location).path == url_for("users_page.users")


@patch("webroutes.users.webapi")
def test_web_users_post_delete_success(mock, client, admin_token):
    mock.return_value = {}
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.post(
        "/settings/users/",
        data=dict(user_id="000000000000000000000000", action="delete", csrf="pytest"),
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert urlparse(response.location).path == url_for("users_page.users")


@patch("webroutes.users.webapi")
def test_web_users_post_unexpected(mock, client, admin_token):
    mock.return_value = {}
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.post(
        "/settings/users/", data=dict(action="unexpected", csrf="pytest")
    )
    assert response.status_code == 200
    assert b"Unexpected error occurred." in response.data


@patch("webroutes.users.webapi", side_effect=Exception("mock exception"))
def test_web_users_post_exception(mock, client, admin_token):
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.post(
        "/settings/users/",
        data=dict(
            user_email="pytest_viewer@example.com",
            user_role="Viewer",
            user_first_name="PyTestFirstName",
            user_last_name="PyTestLastName",
            user_password="pytestpassword",
            action="add",
            csrf="pytest",
        ),
    )
    assert response.status_code == 200
    assert b"mock exception" in response.data
