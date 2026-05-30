from datetime import datetime, timezone
from statistics import median

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from sqlalchemy.orm import selectinload

from app.models import Location, Measurement, Sensor, SyncLog
from app.schemas import HealthResponse, MapPoint, NationalStats, SensorDetail, SyncResult
from app.services.aqi import pm25_quality, quality_bucket
from app.services.sync import run_sync

router = APIRouter(prefix="/api")


@router.get("/health", response_model=HealthResponse)
async def health(db: AsyncSession = Depends(get_db)):
    db_status = "ok"
    try:
        await db.execute(select(func.count()).select_from(Sensor))
    except Exception:
        db_status = "error"

    last_sync = (
        await db.execute(
            select(SyncLog.finished_at)
            .where(SyncLog.status == "success")
            .order_by(desc(SyncLog.finished_at))
            .limit(1)
        )
    ).scalar_one_or_none()

    return HealthResponse(
        status="ok" if db_status == "ok" else "degraded",
        database=db_status,
        last_sync=last_sync,
    )


@router.post("/sync", response_model=SyncResult)
async def trigger_sync(db: AsyncSession = Depends(get_db)):
    log = await run_sync(db)
    return SyncResult(
        status=log.status,
        records_fetched=log.records_fetched or 0,
        records_saved=log.records_saved or 0,
        message="Synchronizacja zakonczona" if log.status == "success" else log.error_message or "",
    )


@router.get("/map", response_model=list[MapPoint])
async def map_points(db: AsyncSession = Depends(get_db), pm_only: bool = True):
    subq = (
        select(
            Measurement.sensor_id,
            func.max(Measurement.measured_at).label("max_time"),
        )
        .group_by(Measurement.sensor_id)
        .subquery()
    )

    stmt = (
        select(Measurement, Sensor, Location)
        .join(Sensor, Sensor.id == Measurement.sensor_id)
        .join(Location, Location.id == Sensor.location_id)
        .join(subq, (Measurement.sensor_id == subq.c.sensor_id) & (Measurement.measured_at == subq.c.max_time))
    )
    if pm_only:
        stmt = stmt.where(Measurement.pm25.isnot(None))

    rows = (await db.execute(stmt)).all()
    points: list[MapPoint] = []
    for measurement, sensor, location in rows:
        label, color = pm25_quality(float(measurement.pm25) if measurement.pm25 else None)
        points.append(
            MapPoint(
                sensor_id=sensor.id,
                location_id=location.id,
                latitude=float(location.latitude),
                longitude=float(location.longitude),
                sensor_type=sensor.sensor_type,
                indoor=location.indoor,
                measured_at=measurement.measured_at,
                pm10=float(measurement.pm10) if measurement.pm10 is not None else None,
                pm25=float(measurement.pm25) if measurement.pm25 is not None else None,
                aqi_level=label,
                aqi_color=color,
            )
        )
    return points


@router.get("/stats", response_model=NationalStats)
async def national_stats(db: AsyncSession = Depends(get_db)):
    subq = (
        select(
            Measurement.sensor_id,
            func.max(Measurement.measured_at).label("max_time"),
        )
        .group_by(Measurement.sensor_id)
        .subquery()
    )

    latest = (
        select(Measurement.pm25, Measurement.pm10, Measurement.measured_at)
        .join(subq, (Measurement.sensor_id == subq.c.sensor_id) & (Measurement.measured_at == subq.c.max_time))
        .where(Measurement.pm25.isnot(None))
    )
    rows = (await db.execute(latest)).all()

    pm25_vals = [float(r.pm25) for r in rows if r.pm25 is not None]
    pm10_vals = [float(r.pm10) for r in rows if r.pm10 is not None]

    by_quality: dict[str, int] = {}
    for v in pm25_vals:
        b = quality_bucket(v)
        by_quality[b] = by_quality.get(b, 0) + 1

    total_sensors = (await db.execute(select(func.count()).select_from(Sensor))).scalar() or 0
    last_sync = (
        await db.execute(
            select(SyncLog.finished_at)
            .where(SyncLog.status == "success")
            .order_by(desc(SyncLog.finished_at))
            .limit(1)
        )
    ).scalar_one_or_none()

    measured_times = [r.measured_at for r in rows if r.measured_at]
    time_range = None
    if measured_times:
        tmin, tmax = min(measured_times), max(measured_times)
        time_range = f"{tmin.isoformat()} - {tmax.isoformat()}"

    return NationalStats(
        total_sensors=total_sensors,
        active_pm_sensors=len(pm25_vals),
        avg_pm25=round(sum(pm25_vals) / len(pm25_vals), 2) if pm25_vals else None,
        avg_pm10=round(sum(pm10_vals) / len(pm10_vals), 2) if pm10_vals else None,
        median_pm25=round(median(pm25_vals), 2) if pm25_vals else None,
        max_pm25=max(pm25_vals) if pm25_vals else None,
        min_pm25=min(pm25_vals) if pm25_vals else None,
        last_sync=last_sync,
        measured_at_range=time_range,
        by_quality=by_quality,
    )


@router.get("/sensors/{sensor_id}", response_model=SensorDetail)
async def sensor_detail(sensor_id: int, db: AsyncSession = Depends(get_db)):
    sensor = (
        await db.execute(
            select(Sensor).options(selectinload(Sensor.location)).where(Sensor.id == sensor_id)
        )
    ).scalar_one_or_none()
    if not sensor:
        raise HTTPException(status_code=404, detail="Czujnik nie znaleziony")

    location = sensor.location
    history_rows = (
        await db.execute(
            select(Measurement)
            .where(Measurement.sensor_id == sensor_id)
            .order_by(desc(Measurement.measured_at))
            .limit(48)
        )
    ).scalars().all()

    latest_point = None
    history = []
    for i, m in enumerate(history_rows):
        entry = {
            "measured_at": m.measured_at.isoformat(),
            "pm10": float(m.pm10) if m.pm10 is not None else None,
            "pm25": float(m.pm25) if m.pm25 is not None else None,
            "temperature": float(m.temperature) if m.temperature is not None else None,
            "humidity": float(m.humidity) if m.humidity is not None else None,
        }
        history.append(entry)
        if i == 0:
            label, color = pm25_quality(float(m.pm25) if m.pm25 else None)
            latest_point = MapPoint(
                sensor_id=sensor.id,
                location_id=location.id,
                latitude=float(location.latitude),
                longitude=float(location.longitude),
                sensor_type=sensor.sensor_type,
                indoor=location.indoor,
                measured_at=m.measured_at,
                pm10=float(m.pm10) if m.pm10 is not None else None,
                pm25=float(m.pm25) if m.pm25 is not None else None,
                aqi_level=label,
                aqi_color=color,
            )

    return SensorDetail(
        sensor_id=sensor.id,
        sensor_type=sensor.sensor_type,
        manufacturer=sensor.manufacturer,
        latitude=float(location.latitude),
        longitude=float(location.longitude),
        indoor=location.indoor,
        latest=latest_point,
        history=history,
    )
