import pytest

# from unittest.mock import patch
from fastapi import HTTPException

from src.api.routes.deploy import update_existing_service


def test_deploy_update_existing_service_success():
    deployment = {
        "account": "Example",
        "application": "Sample",
        "service": "Api",
        "environment": "Dev",
        "status": "Deployed",
        "version": "v9.0.0",
        "timestamp": "1617195244",
        "custom": None,
    }
    response = update_existing_service(deployment)
    # TODO: Query the db to make sure the service write was as expected.
    assert response == 1


def test_deploy_update_existing_service_missing():
    deployment = {
        "account": "MissingAccount",
        "application": "MissingApplication",
        "service": "MissingService",
        "environment": "Dev",
        "status": "Deployed",
        "version": "v9.0.0",
        "timestamp": "1617195244",
        "custom": None,
    }
    with pytest.raises(HTTPException):
        response = update_existing_service(deployment)
        # TODO: Query the db to make sure the service write was as expected.
        assert type(response) is HTTPException
        assert response.status_code == 500
        assert (
            response.detail == "Unexpected error occurred: No matching service found 0."
        )


# TODO: Mock the db exception.
# @patch("routes.deploy.db", side_effect=Exception('mock'))
# def test_deploy_update_existing_service_exception(mock):
#     deployment = {
#         "account": "Example",
#         "application": "PyTestNewApplication",
#         "service": "PyTestNewService",
#         "environment": "PyTest",
#         "status": "Deploying",
#         "version": "v1.0.0",
#         "timestamp": "1617195244",
#         "custom": None
#     }
#     with pytest.raises(HTTPException):
#         response = update_existing_service(deployment)
#         assert response.status_code == 500
#         assert response.json() == {"detail": "Unexpected error occurred."}
#         assert mock.called_once()
