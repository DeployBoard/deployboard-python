from unittest.mock import patch
from flask import url_for
from urllib.parse import urlparse


# TODO: We can add some more tests for this.
@patch('webroutes.applications.webapi')
def test_web_applications_post_success(mock, client, admin_token):
    mock.return_value = [
        {
            "schema_version": 1,
            "service": "Api",
            "application": "Sample",
            "account": "Example",
            "tags": [
                "python"
            ],
            "versions": [
                {
                    "environment": "Dev",
                    "status": "Deployed",
                    "version": "1.3.0",
                    "timestamp": 1608433640,
                    "custom": {
                        "module": "foo",
                        "color": "green"
                    }
                }
            ],
            "_id": "602ec3a41d6ef526c9362d42"
        },
    ]
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['exp'] = 999999999999999
        session['token'] = admin_token
    response = client.post('/applications/', data=dict(
        application_name='pytest',
        service_name='pytest',
        csrf='pytest'
    ), follow_redirects=False)
    assert response.status_code == 302
    assert urlparse(response.location).path == url_for('applications_page.applications')


@patch('webroutes.applications.webapi', side_effect=Exception('mock'))
def test_web_applications_post_exception(mock, client, admin_token):
    data = {
        "application_name": "pytestApplication",
        "service_name": "pytestService"
    }
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['exp'] = 999999999999999
        session['token'] = admin_token
    response = client.post('/applications/', data=data)
    assert response.status_code == 200
    assert b'mock' in response.data
