from unittest.mock import patch


# TODO: Need to refactor the analytics route to be able to make tests better.
@patch("webroutes.analytics.webapi")
def test_web_analytics_get_success(mock, client, admin_token):
    mock.return_value.status_code = 200
    mock.return_value.json.return_value = []
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.get("/analytics/?daysago=7")
    assert response.status_code == 200
    assert b"Analytics" in response.data


@patch("webroutes.analytics.webapi", side_effect=Exception("mock"))
def test_web_analytics_get_exception(mock, client, admin_token):
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.get("/analytics/?daysago=7")
    assert response.status_code == 200
    assert b"mock" in response.data
