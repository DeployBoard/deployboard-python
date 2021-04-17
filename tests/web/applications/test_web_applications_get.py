from unittest.mock import patch


# TODO: This test could be better.
@patch("webroutes.applications.webapi")
def test_web_applications_get_success(mock, client, admin_token):
    mock.return_value.json.return_value = [
        {
            "schema_version": 1,
            "service": "Api",
            "application": "Sample",
            "account": "Example",
            "tags": ["python"],
            "versions": [
                {
                    "environment": "Dev",
                    "status": "Deployed",
                    "version": "1.3.0",
                    "timestamp": 1608433640,
                    "custom": {"module": "foo", "color": "green"},
                }
            ],
            "_id": "602ec3a41d6ef526c9362d42",
        }
    ]
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.get("/applications/")
    assert response.status_code == 200
    assert b"Applications" in response.data


@patch("webroutes.applications.webapi", side_effect=Exception("mock"))
def test_web_applications_get_services_exception(mock, client, admin_token):
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.get("/applications/")
    assert response.status_code == 200
    assert b"mock" in response.data
