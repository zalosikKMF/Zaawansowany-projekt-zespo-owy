from datetime import datetime

from pydantic import BaseModel, Field


class MapPoint(BaseModel):
    sensor_id: int
    location_id: int
    latitude: float
    longitude: float
    sensor_type: str
    indoor: bool
    measured_at: datetime
    pm10: float | None = None
    pm25: float | None = None
    aqi_level: str
    aqi_color: str


class NationalStats(BaseModel):
    total_sensors: int
    active_pm_sensors: int
    avg_pm25: float | None
    avg_pm10: float | None
    median_pm25: float | None
    max_pm25: float | None
    min_pm25: float | None
    last_sync: datetime | None
    measured_at_range: str | None = None
    by_quality: dict[str, int] = Field(default_factory=dict)


class SensorDetail(BaseModel):
    sensor_id: int
    sensor_type: str
    manufacturer: str | None
    latitude: float
    longitude: float
    indoor: bool
    latest: MapPoint | None
    history: list[dict]


class SyncResult(BaseModel):
    status: str
    records_fetched: int
    records_saved: int
    message: str


class HealthResponse(BaseModel):
    status: str
    database: str
    last_sync: datetime | None
