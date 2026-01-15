from pymongo import MongoClient
from datetime import datetime
import os

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "smartfarm")

_client = None

def get_client():
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    return _client

def get_db():
    client = get_client()
    return client[MONGO_DB]

def get_sensor_collection():
    return get_db()["sensor_readings"]

def get_alert_collection():
    return get_db()["alerts"]

def save_reading(data: dict):
    doc = dict(data)
    doc.setdefault("timestamp", datetime.utcnow())
    get_sensor_collection().insert_one(doc)

def save_alert(alert: dict):
    alert_doc = dict(alert)
    alert_doc["timestamp"] = datetime.utcnow()
    get_alert_collection().insert_one(alert_doc)








