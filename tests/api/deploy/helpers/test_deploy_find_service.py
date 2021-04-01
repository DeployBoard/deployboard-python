# import pytest
# from unittest.mock import patch
# from fastapi import HTTPException
from src.api.routes.deploy import find_service


def test_deploy_find_service_success():
    response = find_service(account="Example", application="Sample", service="Api")
    assert type(response) is dict
    assert 'environments' in response


def test_deploy_find_service_missing():
    response = find_service(account="Missing", application="Missing", service="Missing")
    assert response is None


# TODO: Mock the db response to return multiple objects so count > 1.
# @patch("routes.deploy.db", side_effect=({'object1':'1','object2':'2'}))
# def test_deploy_find_service_exception(mock):
#     response = find_service("Example", "Sample", "Api")
#     assert response.status_code == 500
#     assert response.json() == {"detail": "Unexpected error occurred."}
#     assert mock.called_once()


# TODO: Mock the db exception.
# @patch("routes.deploy.db", side_effect=Exception('mock'))
# def test_deploy_find_service_exception(mock):
#     with pytest.raises(HTTPException):
#         response = find_service("MissingAccount", "MissingApplication", "MissingService")
#         assert response.status_code == 500
#         assert response.json() == {"detail": "Unexpected error occurred."}
#         assert mock.called_once()
