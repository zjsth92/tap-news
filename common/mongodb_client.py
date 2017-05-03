import os
import json
from pymongo import MongoClient

with open(os.path.join(os.path.dirname(__file__), '..', 'config.json')) as config_file:    
    config = json.load(config_file)

MONGO_DB_HOST = config["mongodb"]["host"]
MONGO_DB_PORT = config["mongodb"]["port"]
MONGO_DB_USER = os.getenv("MONGODB_USER", '')
MONGO_DB_PASS = os.getenv("MONGODB_PASS", '')

DB_NAME = config["mongodb"]["db_name"]
MONGO_DB_URL = "mongodb://%s:%s@%s:%s/%s" % (MONGO_DB_USER, MONGO_DB_PASS, MONGO_DB_HOST, MONGO_DB_PORT, DB_NAME)
print "Connect to mongodb: %s" % MONGO_DB_URL
client = MongoClient(MONGO_DB_URL)

def get_db(db=DB_NAME):
    db = client[db]
    return db