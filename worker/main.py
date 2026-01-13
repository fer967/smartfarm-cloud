import redis
import json
from worker.services.telemetry_processor import process_telemetry
import os
import time
from app.core.logging_config import setup_logging
import logging

setup_logging()  # 👈 OBLIGATORIO si el worker corre separado

logger = logging.getLogger(__name__)

def process_telemetry(data):
    logger.info("Telemetry processed")
    if not data:
        logger.error("Something failed")

REDIS_HOST = os.getenv("REDIS_HOST")

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    decode_responses=True
)

STREAM_NAME= os.getenv("STREAM_NAME")
CONSUMER_GROUP= os.getenv
CONSUMER_NAME= os.getenv("CONSUMER_NAME")


def create_group():
    while True:
        try:
            redis_client.xgroup_create(
                STREAM_NAME,
                CONSUMER_GROUP,
                id="0",
                mkstream=True
            )
            print("Consumer group creado")
            break
        except redis.exceptions.ResponseError as e:
            if "BUSYGROUP" in str(e):
                print("Consumer group ya existe")
                break
            print("Esperando Redis...")
            time.sleep(2)

def consume():
    print("👂 Esperando eventos de Redis...", flush=True)
    while True:
        messages = redis_client.xreadgroup(
            CONSUMER_GROUP,
            CONSUMER_NAME,
            {STREAM_NAME: ">"},
            count=1,
            block=5000
        )
        for _, entries in messages:
            for message_id, data in entries:
                print(f"📩 Evento recibido: {data}", flush=True)
                payload = json.loads(data["payload"])
                process_telemetry(payload)
                redis_client.xack(STREAM_NAME, CONSUMER_GROUP, message_id)
                print(f"✅ Evento procesado y confirmado: {message_id}", flush=True)

if __name__ == "__main__":
    print("Iniciando worker...")
    create_group()
    consume()








