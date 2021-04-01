# import pytest
# from unittest.mock import patch
# from fastapi import HTTPException
from bson import ObjectId
from src.api.routes.deploy import create_new_service


def test_deploy_create_new_service():
    deployment = {
        "account": "Example",
        "application": "PyTestNewApplication",
        "service": "PyTestNewService",
        "environment": "PyTest",
        "status": "Deploying",
        "version": "v1.0.0",
        "timestamp": "1617195244",
        "custom": None
    }
    response = create_new_service(deployment)
    # TODO: Query the db to make sure the service write was as expected.
    assert type(response) is ObjectId


# TODO: Mock the db exception.
# @patch("routes.deploy.db", side_effect=Exception('mock'))
# def test_deploy_create_new_service_exception(mock):
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
#         response = create_new_service(deployment)
#         assert response.status_code == 500
#         assert response.json() == {"detail": "Unexpected error occurred."}
#         assert mock.called_once()
