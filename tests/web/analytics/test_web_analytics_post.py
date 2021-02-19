from flask import url_for
from urllib.parse import urlparse


# TODO: We can add some more tests for this.
def test_web_analytics_post_success(client):
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['exp'] = 999999999999999
    response = client.post('/analytics/', data=dict(
        application='pytest',
        service='pytest',
        environment='pytest',
        daysago=7,
        csrf='pytest'
    ), follow_redirects=False)
    assert response.status_code == 302
    assert urlparse(response.location).path == url_for('analytics_page.analytics')
    assert 'application=pytest' in response.location
    assert 'service=pytest' in response.location
    assert 'environment=pytest' in response.location
    assert 'daysago=7' in response.location
