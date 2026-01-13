from datetime import datetime
from app.db.mongo import dead_letters

MAX_RETRIES = 3

def process_with_retry(data: dict, retries=0):
    try:
        # lógica principal
        ...
    except Exception as e:
        if retries < MAX_RETRIES:
            process_with_retry(data, retries + 1)
        else:
            dead_letters.insert_one({
                "payload": data,
                "error": str(e),
                "retries": retries,
                "timestamp": datetime.utcnow()
            })
