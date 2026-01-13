from pymongo import MongoClient
from datetime import datetime
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB", "smartfarm")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

sensor_collection = db["sensor_readings"]
alert_collection = db["alerts"]

def save_reading(data: dict):
    doc = dict(data)

    # 🔥 FIX CLAVE
    if not doc.get("timestamp"):
        doc["timestamp"] = datetime.utcnow()

    sensor_collection.insert_one(doc)

def save_alert(alert: dict):
    alert_doc = dict(alert)
    alert_doc["timestamp"] = datetime.utcnow()
    alert_collection.insert_one(alert_doc)







