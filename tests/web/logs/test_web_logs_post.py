from urllib.parse import urlparse

from flask import url_for


# TODO: We can add some more tests for this.
def test_web_logs_post_success(client):
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
    response = client.post(
        "/logs/",
        data=dict(
            application="pytest", service="pytest", environment="pytest", csrf="pytest"
        ),
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert urlparse(response.location).path == url_for("logs_page.logs")
    assert "application=pytest" in response.location
    assert "service=pytest" in response.location
    assert "environment=pytest" in response.location
