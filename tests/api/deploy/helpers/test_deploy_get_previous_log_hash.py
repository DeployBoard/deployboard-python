import pytest
from unittest.mock import patch
from fastapi import HTTPException
from src.api.routes.deploy import get_previous_log_hash


def test_deploy_get_previous_log_hash_new_log():
    # Should return an empty string
    response = get_previous_log_hash("Example", "PyTest", "PyTest", "PyTest")
    assert type(response) is str
    assert len(response) == 0


def test_deploy_get_previous_log_hash_existing_log():
    # Note this is the same as the above test, so there should be an existing sha256 hash to return.
    response = get_previous_log_hash("Example", "Sample", "Api", "Dev")
    assert type(response) is str
    assert len(response) == 64
    assert response is not ''


# TODO: Mock the db response so there are 2 returned so we raise the critical error.

# TODO: Mock the db exception.
# @patch("routes.deploy.db", side_effect=Exception('mock'))
# def test_deploy_get_previous_log_hash_exception(mock):
#     with pytest.raises(HTTPException):
#         response = handle_environment("MissingAccount", "PyTest")
#         assert response.status_code == 500
#         assert response.json() == {"detail": "Unexpected error occurred."}
#         assert mock.called_once()
