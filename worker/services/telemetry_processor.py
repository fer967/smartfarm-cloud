from datetime import datetime
from worker.db.mongo import save_reading, save_alert

def process_telemetry(data: dict):
    doc = dict(data)
    if not doc.get("timestamp"):
        doc["timestamp"] = datetime.utcnow()
    save_reading(doc)
    if doc.get("water_low") is True:
        save_alert({
            "type": "LOW_WATER_LEVEL",
            "device_id": doc.get("device_id"),
            "value": doc.get("water_distance"),
            "timestamp": datetime.utcnow()
        })







