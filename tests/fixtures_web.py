import pytest
from web.main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        with app.app_context():
            pass
        yield client


@pytest.fixture
def admin_username():
    return 'admin@example.com'


@pytest.fixture
def editor_username():
    return 'editor@example.com'


@pytest.fixture
def viewer_username():
    return 'viewer@example.com'


@pytest.fixture
def password():
    return 'secret'
