import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


@pytest.mark.order('first')
def test_first(seed_data):
    assert 'account' in seed_data
    assert 'users' in seed_data
    assert 'api_keys' in seed_data


@pytest.mark.order('second')
def test_second(admin_token, editor_token, viewer_token, user):
    assert admin_token is not None
    assert editor_token is not None
    assert viewer_token is not None
    assert user is not None
