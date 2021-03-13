import os
from unittest import mock
from src.api.db import mongo
from pymongo.database import Database


# TODO: This is not covering what is expected.
@mock.patch.dict(os.environ, {"MONGO_URI": "pytest"})
def test_db_pymongo():
    assert mongo.db is not None
    assert type(mongo.db) is Database


def test_db_pymongo_inmemory():
    assert mongo.db is not None
    assert type(mongo.db) is Database
