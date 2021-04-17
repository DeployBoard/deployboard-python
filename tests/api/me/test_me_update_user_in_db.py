from unittest.mock import patch

import pytest
from bson import ObjectId
from fastapi import HTTPException

from api.routes.me import update_user_in_db


def test_me_update_user_in_db_valid(user):
    updates = {"first_name": "pytest"}
    query = {"_id": ObjectId(user)}
    update_command = {"$set": updates}
    response = update_user_in_db(query, update_command)
    assert type(response) is dict
    assert response["modified_count"] == "1"


@patch("api.routes.me.db")
def test_me_update_user_in_db_exception(mock, user):
    updates = {"first_name": "pytest"}
    query = {"_id": ObjectId(user)}
    update_command = {"$set": updates}
    mock.users.update_one.side_effect = Exception("mock")
    with pytest.raises(HTTPException):
        response = update_user_in_db(query, update_command)
        # TODO: This test covers the exception, but does not enforce these assertions.
        assert type(response) is HTTPException
        assert response.status_code == 500
        assert response.json()["detail"] == "Unexpected error occurred."
