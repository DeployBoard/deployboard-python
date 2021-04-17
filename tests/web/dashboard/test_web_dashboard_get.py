from unittest.mock import patch


@patch("webroutes.dashboard.webapi")
def test_web_dashboard_get_success(mock, client, admin_token):
    mock.return_value = [
        {
            "schema_version": 1,
            "service": "Api",
            "application": "Admin",
            "account": "Example",
            "tags": ["python"],
            "environments": {
                "Prod": {
                    "status": "Deployed",
                    "version": "1.2.0",
                    "timestamp": 1608623640,
                    "custom": {"module": "foo", "color": "green"},
                }
            },
            "_id": "602ec3a41d6ef526c9362d42",
        }
    ]
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.get("/dashboard/")
    assert response.status_code == 200
    assert b"Dashboard" in response.data
    assert b"Admin" in response.data
    assert b"Prod" in response.data
    assert b"Deployed" in response.data


@patch("webroutes.dashboard.webapi", side_effect=Exception("mock"))
def test_dashboard_get_exception(mock, client, admin_token):
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.get("/dashboard/")
    assert response.status_code == 200
    assert b"mock" in response.data
