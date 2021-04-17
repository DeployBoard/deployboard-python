from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


# GET /logs/
def test_get_logs_admin(admin_token):
    response = client.get("/logs/", headers={"Authorization": admin_token})
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_logs_editor(editor_token):
    response = client.get("/logs/", headers={"Authorization": editor_token})
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_logs_viewer(viewer_token):
    response = client.get("/logs/", headers={"Authorization": viewer_token})
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_logs_filter_application(admin_token):
    query_string = "?application=Sample"
    response = client.get(
        f"/logs/{query_string}", headers={"Authorization": admin_token}
    )
    assert response.status_code == 200
    assert type(response.json()) == list
    assert response.json()[0]["application"] == "Sample"


def test_get_logs_filter_service(admin_token):
    query_string = "?service=Api"
    response = client.get(
        f"/logs/{query_string}", headers={"Authorization": admin_token}
    )
    assert response.status_code == 200
    assert type(response.json()) == list
    assert response.json()[0]["service"] == "Api"


def test_get_logs_filter_environment(admin_token):
    query_string = "?environment=Dev"
    response = client.get(
        f"/logs/{query_string}", headers={"Authorization": admin_token}
    )
    assert response.status_code == 200
    assert type(response.json()) == list
    assert response.json()[0]["environment"] == "Dev"


def test_get_logs_filter_status(admin_token):
    query_string = "?status=Deployed"
    response = client.get(
        f"/logs/{query_string}", headers={"Authorization": admin_token}
    )
    assert response.status_code == 200
    assert type(response.json()) == list
    assert response.json()[0]["status"] == "Deployed"


def test_get_logs_filter_sort_ascending(admin_token):
    query_string = "?sort=1"
    response = client.get(
        f"/logs/{query_string}", headers={"Authorization": admin_token}
    )
    assert response.status_code == 200
    assert type(response.json()) == list
    assert response.json()[0]["timestamp"] < response.json()[-1]["timestamp"]


def test_get_logs_filter_sort_descending(admin_token):
    query_string = "?sort=-1"
    response = client.get(
        f"/logs/{query_string}", headers={"Authorization": admin_token}
    )
    assert response.status_code == 200
    assert type(response.json()) == list
    assert response.json()[0]["timestamp"] > response.json()[-1]["timestamp"]


def test_get_logs_filter_sort_invalid(admin_token):
    query_string = "?sort=999"
    response = client.get(
        f"/logs/{query_string}", headers={"Authorization": admin_token}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "sort must be -1 or 1, provided 999"


def test_get_logs_filter_from_timestamp(admin_token):
    query_string = "?from_timestamp=0"
    response = client.get(
        f"/logs/{query_string}", headers={"Authorization": admin_token}
    )
    assert response.status_code == 200
    assert type(response.json()) == list
    assert response.json()[0]["timestamp"] > 0


def test_get_logs_filter_to_timestamp(admin_token):
    query_string = "?to_timestamp=9999999999"
    response = client.get(
        f"/logs/{query_string}", headers={"Authorization": admin_token}
    )
    assert response.status_code == 200
    assert type(response.json()) == list
    assert response.json()[0]["timestamp"] < 9999999999


def test_get_logs_filter_from_and_to_timestamp(admin_token):
    query_string = "?from_timestamp=0&to_timestamp=9999999999"
    response = client.get(
        f"/logs/{query_string}", headers={"Authorization": admin_token}
    )
    assert response.status_code == 200
    assert type(response.json()) == list
    assert response.json()[0]["timestamp"] > 0
    assert response.json()[0]["timestamp"] < 9999999999


def test_get_logs_filter_multiple(admin_token):
    query_string = (
        "?application=Sample&service=Api&from_timestamp=0&to_timestamp=9999999999"
    )
    response = client.get(
        f"/logs/{query_string}", headers={"Authorization": admin_token}
    )
    assert response.status_code == 200
    assert type(response.json()) == list
    assert response.json()[0]["application"] == "Sample"
    assert response.json()[0]["service"] == "Api"
    assert response.json()[0]["timestamp"] > 0
    assert response.json()[0]["timestamp"] < 9999999999


def test_get_logs_bad_token():
    response = client.get("/logs/", headers={"Authorization": "bad-token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
