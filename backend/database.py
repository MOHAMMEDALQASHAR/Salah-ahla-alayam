import os
import certifi
from dotenv import load_dotenv

# Load .env file if it exists (for local development)
load_dotenv()

from pymongo import MongoClient

DEFAULT_URI = (
    "mongodb+srv://alqashar0_db_user:Mtm775070_981@"
    "cluster0.gcalylm.mongodb.net/ahla_alayam?retryWrites=true&w=majority&appName=Cluster0"
)

MONGODB_URI = os.getenv("MONGODB_URI", DEFAULT_URI).strip()
if not MONGODB_URI:
    MONGODB_URI = DEFAULT_URI

_client = None
_db = None

def _get_client():
    global _client
    if _client is None:
        _client = MongoClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000,
            socketTimeoutMS=10000,
            maxPoolSize=10,
            retryWrites=True,
            tls=True,
            tlsCAFile=certifi.where(),
        )
    return _client

def get_db():
    global _db
    if _db is None:
        client = _get_client()
        db_name = os.getenv("MONGODB_DB_NAME", "ahla_alayam")
        _db = client[db_name]
    return _db
