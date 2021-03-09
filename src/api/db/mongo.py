from util.config import config

# If you pass mongo_uri we use that.
if config("MONGO_URI"):
    from pymongo import MongoClient
    client = MongoClient(config("MONGO_URI"))
# Else we use inmemory. This is really just used for testing.
else:
    from pymongo_inmemory import MongoClient
    client = MongoClient()

db = client[config("MONGO_DATABASE")]
