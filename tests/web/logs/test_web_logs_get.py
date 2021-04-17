from unittest.mock import patch


# TODO: This test could be better. I think issue with calling same function twice?
@patch("webroutes.logs.webapi")
@patch("webroutes.logs.webapi")
def test_web_logs_get_success(mock_get_logs, mock_get_services, client, admin_token):
    mock_get_logs.return_value = []
    mock_get_services.return_value = []
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.get("/logs/")
    assert response.status_code == 200
    assert b"Logs" in response.data


@patch("webroutes.logs.webapi", side_effect=Exception("mock"))
def test_web_environments_get_exception(mock, client, admin_token):
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.get("/logs/")
    assert response.status_code == 200
    assert b"mock" in response.data
