from unittest.mock import patch


@patch("webroutes.apikeys.webapi")
def test_web_apikeys_get_single_success(mock, client, admin_token, apikey):
    mock.return_value.json.return_value = {}
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.get(f"/settings/apikeys/{apikey}")
    assert response.status_code == 200
    assert b"Name" in response.data
    assert b"Key" in response.data
    assert b"Role" in response.data
    assert b"Enabled" in response.data


@patch("webroutes.apikeys.webapi", side_effect=Exception("mock"))
def test_web_apikeys_get_single_exception(mock, client, admin_token, apikey):
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.get(f"/settings/apikeys/{apikey}")
    assert response.status_code == 200
    assert b"mock" in response.data
