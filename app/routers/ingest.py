from fastapi import APIRouter, Header, HTTPException
from app.schemas.telemetry import TelemetryIn
from app.core.redis import redis_client
from datetime import datetime
import os
import json

router = APIRouter(prefix="/ingest", tags=["Ingest"])

STREAM_NAME = "telemetry-events"
DEVICE_API_KEY = os.getenv("DEVICE_API_KEY")

@router.post("/telemetry", status_code=202)
def ingest_telemetry(
    telemetry: TelemetryIn,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    if x_api_key != DEVICE_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    data = telemetry.model_dump(exclude_none=True)
    data["timestamp"] = datetime.utcnow().isoformat()

    redis_client.xadd(
        STREAM_NAME,
        {
            "device_id": data["device_id"],
            "payload": json.dumps(data)
        }
    )

    return {"status": "accepted"}


