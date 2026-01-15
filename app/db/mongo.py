from pymongo import MongoClient
from app.core.config import MONGO_URI, MONGO_DB

_client = None

def get_client():
    global _client
    if _client is None:
        _client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=3000
        )
    return _client

def get_db():
    return get_client()[MONGO_DB]

def get_sensor_readings():
    return get_db().sensor_readings

def get_dead_letters():
    return get_db().dead_letters








