# import pytest
# from unittest.mock import patch
# from fastapi import HTTPException
from src.api.routes.deploy import insert_to_logs


def test_deploy_insert_to_logs():
    log = {
        "application": "PyTestDeployApp",
        "service": "PyTestDeployService",
        "environment": "PyTest",
        "status": "Deploying",
        "version": "v1.0.2",
    }
    response = insert_to_logs(log)
    # TODO: Query the db to make sure the log write was as expected.
    assert response is None


# TODO: Mock the db exception.
# @patch("routes.deploy.db", side_effect=Exception('mock'))
# def test_deploy_insert_to_logs_exception(mock):
#     with pytest.raises(HTTPException):
#         response = insert_to_logs("MissingAccount", "PyTest")
#         assert response.status_code == 500
#         assert response.json() == {"detail": "Unexpected error occurred."}
#         assert mock.called_once()
