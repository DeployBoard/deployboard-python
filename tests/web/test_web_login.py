# import pytest
# from fastapi.testclient import TestClient
# from web.main import app
#
# client = TestClient(app)
#
#
# def test_web_login():
#     response = client.get("/login")
#     assert response.status_code == 200
#     assert 'Username' in response.data
