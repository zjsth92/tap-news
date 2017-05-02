import os
import json
from pymongo import MongoClient

with open(os.path.join(os.path.dirname(__file__), '..', 'config.json')) as config_file:    
    config = json.load(config_file)

MONGO_DB_HOST = config["mongodb"]["host"]
MONGO_DB_PORT = config["mongodb"]["port"]
DB_NAME = config["mongodb"]["db_name"]

client = MongoClient("%s:%s" % (MONGO_DB_HOST, MONGO_DB_PORT))

def get_db(db=DB_NAME):
    db = client[db]
    return db