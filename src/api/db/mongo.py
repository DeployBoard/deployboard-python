import os

if 'DPB_ENV' in os.environ and os.environ['DPB_ENV'] == 'pytest':
    from pymongo_inmemory import MongoClient
    client = MongoClient()
else:
    from pymongo import MongoClient
    client = MongoClient(os.environ['MONGO_URI'])

db = client.deployboard
