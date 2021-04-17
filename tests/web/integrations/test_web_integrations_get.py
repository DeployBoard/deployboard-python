def test_web_integrations_get_success(client, admin_token):
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["exp"] = 999999999999999
        session["token"] = admin_token
    response = client.get("/settings/integrations/")
    assert response.status_code == 200


# TODO: Add this test when we lock the integrations route.
# def test_web_integrations_get_unauthorized_viewer(client, viewer_token):
#     with client.session_transaction() as session:
#         session['logged_in'] = True
#         session['exp'] = 999999999999999
#         session['token'] = viewer_token
#     response = client.get('/settings/integrations/')
#     assert response.status_code == 403
#     assert b'Unauthorized' in response.data
#
#
# TODO: Add this test when we lock the integrations route.
# def test_web_integrations_get_unauthorized_editor(client, editor_token):
#     with client.session_transaction() as session:
#         session['logged_in'] = True
#         session['exp'] = 999999999999999
#         session['token'] = editor_token
#     response = client.get('/settings/integrations/')
#     assert response.status_code == 403
#     assert b'Unauthorized' in response.data
