from unittest.mock import patch
from urllib.parse import urlparse

from flask import url_for


@patch("webroutes.environments.webapi")
def test_web_environments_post_up_success(mock, client, admin_token):
    mock.return_value = {}
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.post(
        "/settings/environments/",
        data=dict(
            environment_name="PyTest2",
            environment_list="['PyTest1', 'PyTest2', 'PyTest3']",
            action="up",
            csrf="pytest",
        ),
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert urlparse(response.location).path == url_for("environments_page.environments")


@patch("webroutes.environments.webapi")
def test_web_environments_post_up_already_top(mock, client, admin_token):
    mock.return_value = {}
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.post(
        "/settings/environments/",
        data=dict(
            environment_name="PyTest1",
            environment_list="['PyTest1', 'PyTest2', 'PyTest3']",
            action="up",
            csrf="pytest",
        ),
        follow_redirects=False,
    )
    assert response.status_code == 200
    assert b"PyTest1 is already top priority." in response.data


@patch("webroutes.environments.webapi")
def test_web_environments_post_down_success(mock, client, admin_token):
    mock.return_value = {}
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.post(
        "/settings/environments/",
        data=dict(
            environment_name="PyTest2",
            environment_list="['PyTest1', 'PyTest2', 'PyTest3']",
            action="down",
            csrf="pytest",
        ),
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert urlparse(response.location).path == url_for("environments_page.environments")


@patch("webroutes.environments.webapi")
def test_web_environments_post_down_already_bottom(mock, client, admin_token):
    mock.return_value = {}
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.post(
        "/settings/environments/",
        data=dict(
            environment_name="PyTest3",
            environment_list="['PyTest1', 'PyTest2', 'PyTest3']",
            action="down",
            csrf="pytest",
        ),
        follow_redirects=False,
    )
    assert response.status_code == 200
    assert b"PyTest3 is already lowest priority." in response.data


@patch("webroutes.environments.webapi")
def test_web_environments_post_unexpected(mock, client, admin_token):
    mock.return_value = {}
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.post(
        "/settings/environments/", data=dict(action="unexpected", csrf="pytest")
    )
    assert response.status_code == 200
    assert b"Unexpected error occurred." in response.data


@patch("webroutes.environments.webapi", side_effect=Exception("mock exception"))
def test_web_environments_post_exception(mock, client, admin_token):
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.post(
        "/settings/environments/",
        data=dict(
            environment_name="PyTest2",
            environment_list="['PyTest1', 'PyTest2', 'PyTest3']",
            action="down",
            csrf="pytest",
        ),
        follow_redirects=False,
    )
    assert response.status_code == 200
    assert b"mock exception" in response.data
