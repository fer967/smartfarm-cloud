import json
import redis
from pymongo import MongoClient
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
MONGO_URI = os.getenv("MONGO_URI")

STREAM_NAME = "telemetry-events"
GROUP_NAME = "telemetry_group"
CONSUMER_NAME = "worker-1"

def main():
    print("🚀 Telemetry worker starting...")
    print(f"🔌 Redis host: {REDIS_HOST}")
    print(f"🗄️ Mongo URI: {MONGO_URI}")

    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=6379,
        decode_responses=True
    )

    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client.get_default_database()
    sensor_collection = db.sensor_readings

    # Crear consumer group si no existe
    try:
        redis_client.xgroup_create(
            STREAM_NAME,
            GROUP_NAME,
            id="0",
            mkstream=True
        )
        print("✅ Consumer group created")
    except redis.exceptions.ResponseError as e:
        if "BUSYGROUP" in str(e):
            print("ℹ️ Consumer group already exists")
        else:
            raise

    print("👂 Waiting for telemetry events...")

    while True:
        messages = redis_client.xreadgroup(
            groupname=GROUP_NAME,
            consumername=CONSUMER_NAME,
            streams={STREAM_NAME: ">"},
            count=1,
            block=5000
        )

        if not messages:
            continue

        for _, entries in messages:
            for message_id, fields in entries:
                payload = json.loads(fields["payload"])

                sensor_collection.insert_one(payload)
                redis_client.xack(STREAM_NAME, GROUP_NAME, message_id)

                print(f"📥 Consumed {message_id} → MongoDB")


if __name__ == "__main__":
    main()
