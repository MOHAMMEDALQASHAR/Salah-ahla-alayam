import os
from pymongo import MongoClient

DEFAULT_URI = (
    "mongodb://alqashar0_db_user:Mtm775070_981@"
    "ac-rfe4z7p-shard-00-00.gcalylm.mongodb.net:27017,"
    "ac-rfe4z7p-shard-00-01.gcalylm.mongodb.net:27017,"
    "ac-rfe4z7p-shard-00-02.gcalylm.mongodb.net:27017/"
    "ahla_alayam?ssl=true&authSource=admin&retryWrites=true&w=majority"
)

MONGODB_URI = os.getenv("MONGODB_URI", DEFAULT_URI)

client = MongoClient(MONGODB_URI)

# Database instance
db_name = os.getenv("MONGODB_DB_NAME", "ahla_alayam")
db = client[db_name]

def get_db():
    return db
