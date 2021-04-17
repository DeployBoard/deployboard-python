from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


# GET /hc/
def test_get_hc():
    response = client.get("/hc/")
    assert response.status_code == 200
