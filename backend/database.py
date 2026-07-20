import os
from pymongo import MongoClient

DEFAULT_URI = (
    "mongodb+srv://alqashar0_db_user:Mtm775070_981@"
    "cluster0.gcalylm.mongodb.net/ahla_alayam?retryWrites=true&w=majority&appName=Cluster0"
)

MONGODB_URI = os.getenv("MONGODB_URI", DEFAULT_URI).strip()
if not MONGODB_URI:
    MONGODB_URI = DEFAULT_URI

client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=10000)

# Database instance
db_name = os.getenv("MONGODB_DB_NAME", "ahla_alayam")
db = client[db_name]

def get_db():
    return db
