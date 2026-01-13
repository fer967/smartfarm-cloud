import redis
import json

redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

STREAM_NAME = "telemetry-events"

def publish_telemetry_event(data: dict):
    redis_client.xadd(
        STREAM_NAME,
        {
            "payload": json.dumps(data)
        }
    )
