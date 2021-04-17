from unittest.mock import patch


@patch("webroutes.users.webapi")
def test_web_users_get_success(mock, client, admin_token):
    mock.return_value.json.return_value = []
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.get("/settings/users/")
    assert response.status_code == 200
    assert b"Users" in response.data
    assert b"Email" in response.data
    assert b"Enabled" in response.data


@patch("webroutes.users.webapi", side_effect=Exception("mock"))
def test_web_users_get_exception(mock, client, admin_token):
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.get("/settings/users/")
    assert response.status_code == 200
    assert b"mock" in response.data
