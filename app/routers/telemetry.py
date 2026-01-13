from fastapi import APIRouter, Request, HTTPException, Depends, BackgroundTasks
from app.db.mongo import sensor_readings, dead_letters 
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.dependencies.roles import require_tecnico, require_admin
from app.core.limiter import limiter
from app.services.telemetry_worker import process_telemetry

router = APIRouter(
    prefix="/telemetry",
    tags=["Telemetry"]
)

templates = Jinja2Templates(directory="app/templates")

def serialize(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@router.post("/telemetry")
def ingest(data: dict, bg: BackgroundTasks):
    bg.add_task(process_telemetry, data)
    return {"status": "accepted"}

@router.get("/sensor-readings")
def list_sensor_readings(limit: int = 50, user=Depends(require_tecnico)):   
    cursor = (
        sensor_readings
        .find()
        .sort("_id", -1)
        .limit(limit)
    )
    return [serialize(doc) for doc in cursor]


@router.get("/view", response_class=HTMLResponse)
def telemetry_view(
    request: Request,
    user=Depends(require_tecnico)
):
    cursor = (
        sensor_readings
        .find()
        .sort("_id", -1)
        .limit(20)
    )
    data = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        data.append(doc)
    return templates.TemplateResponse(
        "telemetry.html",
        {
            "request": request,
            "readings": data,
            "user": user
        }
    )


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    user=Depends(require_tecnico)
):
    last = sensor_readings.find_one(sort=[("_id", -1)])
    if last:
        last["_id"] = str(last["_id"])

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "last": last,
            "user": user
        }
    )


@router.get("/latest", tags=["Telemetry"])
def latest_telemetry(user=Depends(require_tecnico)):    
    last = sensor_readings.find_one(sort=[("_id", -1)])
    if not last:
        return {
            "device_id": None,
            "temperature": None,
            "humidity": None,
            "water_distance": None,
            "water_low": None,
            "timestamp": None
        }
    return {
        "device_id": last.get("device_id"),
        "temperature": last.get("temperature"),
        "humidity": last.get("humidity"),
        "water_distance": last.get("water_distance"),
        "water_low": last.get("water_low"),
        "timestamp": last.get("timestamp")
    }

@router.get("/live", response_class=HTMLResponse, include_in_schema=False)
def telemetry_live(request: Request, user=Depends(require_tecnico)):   
    return templates.TemplateResponse(
        "telemetry_live.html",
        {"request": request}
    )


@router.get("/last")
@limiter.limit("10/minute")                  
def get_last_reading(
    request: Request,
    user=Depends(require_tecnico)
):
    last = sensor_readings.find_one(sort=[("_id", -1)])
    if not last:
        return {}
    last["_id"] = str(last["_id"])
    return last


@router.get("/last-n")
def last_n_readings(
    limit: int = 20,
    user=Depends(require_tecnico)
):
    readings = list(
        sensor_readings
        .find()
        .sort("_id", -1)
        .limit(limit)
    )
    readings.reverse()
    for r in readings:
        r["_id"] = str(r["_id"])
    return readings


@router.get("/health")                      
def health():
    return {
        "status": "ok",
        "service": "smartfarm-api"
    }

@router.get("/dead-letters")                       
def list_dead_letters(user=Depends(require_admin)):
    cursor = dead_letters.find().sort("timestamp", -1).limit(50)
    return [{**d, "_id": str(d["_id"])} for d in cursor]










