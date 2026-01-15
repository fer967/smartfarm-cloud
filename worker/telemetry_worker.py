import json
import redis
import os
from worker.db.mongo import get_sensor_collection

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

STREAM_NAME = os.getenv("STREAM_NAME", "telemetry-events")
GROUP_NAME = os.getenv("CONSUMER_GROUP", "telemetry-workers")
CONSUMER_NAME = os.getenv("CONSUMER_NAME", "worker-1")


def main():
    print("🚀 Telemetry worker starting...")
    print(f"🔌 Redis host: {REDIS_HOST}")

    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        decode_responses=True
    )

    sensor_collection = get_sensor_collection()

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
