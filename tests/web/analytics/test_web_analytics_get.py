from unittest.mock import patch


# TODO: Mock the call to api_get instead of requests.get.
@patch('requests.get')
def test_web_analytics_get_success(mock, client, admin_token):
    mock.return_value.status_code = 200
    mock.return_value.json.return_value = []
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['exp'] = 999999999999999
        session['token'] = admin_token
    response = client.get('/analytics/?daysago=7')
    assert response.status_code == 200
    assert b'Analytics' in response.data

# TODO: Analytics needs to return error if it receives Exception from API.
# @patch('requests.get', side_effect=Exception('mocked error'))
# def test_web_analytics_get_exception(mock, admin_token):
#     with pytest.raises(Exception) as excinfo:
#         with client.session_transaction() as session:
#             session['logged_in'] = True
#             session['exp'] = 999999999999999
#             session['token'] = admin_token
#         response = client.get('/analytics/?daysago=7')
#     assert str(excinfo.value) == 'mocked error'
#     assert response.status_code == 200
#     assert 'mocked error' in response.data
