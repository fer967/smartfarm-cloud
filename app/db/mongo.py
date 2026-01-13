from pymongo import MongoClient
from app.core.config import MONGO_URI, MONGO_DB

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

sensor_readings = db.sensor_readings
dead_letters = db.dead_letters








