import os

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
MONGO_DB = os.getenv("MONGO_DB", "smartfarm")

STREAM_NAME = os.getenv("STREAM_NAME", "telemetry-events")
CONSUMER_GROUP = os.getenv("CONSUMER_GROUP", "telemetry-workers")
CONSUMER_NAME = os.getenv("CONSUMER_NAME", "worker-1")

