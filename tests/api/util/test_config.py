import os
from unittest import mock

from src.api.util.config import config


def test_config_default_mongo_uri():
    response = config("MONGO_URI")
    assert response is None


def test_config_default_mongo_database():
    response = config("MONGO_DATABASE")
    assert response is not None
    assert type(response) == str
    assert response == "deployboard"


@mock.patch.dict(os.environ, {"MONGO_URI": "pytest"})
def test_config_environment():
    response = config("MONGO_URI")
    assert response is not None
    assert type(response) == str
    assert response == "pytest"
