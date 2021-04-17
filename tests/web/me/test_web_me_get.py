from unittest.mock import patch


@patch("webroutes.me.webapi")
def test_web_me_get_success(mock, client, admin_token):
    mock.return_value = {
        "first_name": "MyFirstName",
        "last_name": "MyLastName",
        "avatar": "myAvatar",
        "theme": "Dark",
    }
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.get("/me/")
    assert response.status_code == 200
    assert b"MyFirstName" in response.data
    assert b"MyLastName" in response.data
    assert b"myAvatar" in response.data
    assert b"Dark" in response.data


@patch("webroutes.me.webapi", side_effect=Exception("mock"))
def test_web_me_get_exception(mock, client, admin_token):
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.get("/me/")
    assert response.status_code == 200
    assert b"mock" in response.data
