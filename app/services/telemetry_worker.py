from app.db.mongo import get_sensor_readings, get_dead_letters
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def process_telemetry(data: dict):
    try:
        get_sensor_readings.insert_one({
            **data,
            "processed_at": datetime.utcnow()
        })

        if data.get("water_low"):
            logger.warning("WATER_LOW", extra=data)

    except Exception as e:
        get_dead_letters.insert_one({
            "payload": data,
            "error": str(e),
            "timestamp": datetime.utcnow()
        })
