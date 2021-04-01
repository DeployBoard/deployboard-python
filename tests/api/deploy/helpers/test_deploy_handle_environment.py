import pytest
from unittest.mock import patch
from fastapi import HTTPException
from src.api.routes.deploy import handle_environment


def test_deploy_handle_environment_new():
    # account should have been modified, new environment added to list.
    response = handle_environment("Example", "PyTest")
    assert response is None


def test_deploy_handle_environment_existing():
    # account should not have been modified.
    response = handle_environment("Example", "PyTest")
    assert response is None


def test_deploy_handle_environment_account_missing():
    with pytest.raises(HTTPException):
        response = handle_environment("MissingAccount", "PyTest")
        assert response.status_code is 500
        assert response.json['detail'] == "Unexpected error occurred: No account found 0."


# TODO: Mock the db exception.
# @patch("routes.deploy.db", side_effect=Exception('mock'))
# def test_handle_environment_exception(mock):
#     with pytest.raises(HTTPException):
#         response = handle_environment("MissingAccount", "PyTest")
#         assert response.status_code == 500
#         assert response.json() == {"detail": "Unexpected error occurred."}
#         assert mock.called_once()
