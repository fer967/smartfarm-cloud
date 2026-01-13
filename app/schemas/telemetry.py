from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TelemetryIn(BaseModel):
    device_id: str = Field(..., example="esp32_01")
    temperature: float = Field(..., example=22.5)
    humidity: float = Field(..., example=60.0)

    water_distance: Optional[float] = Field(None, example=8.5)
    water_low: Optional[bool] = Field(None, example=False)

    timestamp: Optional[datetime] = Field(default=None)



