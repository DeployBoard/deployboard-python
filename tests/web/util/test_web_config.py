import os
from unittest import mock

from src.web.webutil.config import config


def test_web_config_default_dpb_api_uri():
    response = config("DPB_API_URI")
    assert response is not None
    assert type(response) == str
    assert response == "http://api:8081"


@mock.patch.dict(os.environ, {"DPB_API_URI": "pytest"})
def test_web_config_environment():
    response = config("DPB_API_URI")
    assert response is not None
    assert type(response) == str
    assert response == "pytest"
