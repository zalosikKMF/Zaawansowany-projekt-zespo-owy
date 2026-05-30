from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models import Location, Measurement, Sensor, SyncLog
from app.services.sensor_community import extract_values, fetch_country_measurements, parse_timestamp


def _upsert_stmt(model, values: dict, index_elements: list, update_cols: dict | None = None):
    if "postgresql" in settings.database_url:
        from sqlalchemy.dialects.postgresql import insert as pg_insert

        stmt = pg_insert(model).values(**values)
        if update_cols:
            return stmt.on_conflict_do_update(index_elements=index_elements, set_=update_cols)
        return stmt.on_conflict_do_nothing(index_elements=index_elements)

    from sqlalchemy.dialects.sqlite import insert as sqlite_insert

    stmt = sqlite_insert(model).values(**values)
    if update_cols:
        return stmt.on_conflict_do_update(index_elements=index_elements, set_=update_cols)
    return stmt.on_conflict_do_nothing(index_elements=index_elements)


async def run_sync(session: AsyncSession, country: str | None = None) -> SyncLog:
    log = SyncLog(status="running", started_at=datetime.now(timezone.utc))
    session.add(log)
    await session.flush()

    saved = 0
    try:
        records = await fetch_country_measurements(country)
        log.records_fetched = len(records)

        for item in records:
            loc = item.get("location") or {}
            sensor_info = item.get("sensor") or {}
            sensor_type = (sensor_info.get("sensor_type") or {}).get("name") or "unknown"
            location_id = loc.get("id")
            sensor_id = sensor_info.get("id")
            if not location_id or not sensor_id:
                continue

            await session.execute(
                _upsert_stmt(
                    Location,
                    {
                        "id": location_id,
                        "latitude": float(loc["latitude"]),
                        "longitude": float(loc["longitude"]),
                        "altitude": float(loc["altitude"]) if loc.get("altitude") else None,
                        "country": loc.get("country", "PL"),
                        "indoor": bool(loc.get("indoor")),
                        "exact_location": bool(loc.get("exact_location")),
                        "updated_at": datetime.now(timezone.utc),
                    },
                    [Location.id],
                    {
                        "latitude": float(loc["latitude"]),
                        "longitude": float(loc["longitude"]),
                        "updated_at": datetime.now(timezone.utc),
                    },
                )
            )

            await session.execute(
                _upsert_stmt(
                    Sensor,
                    {
                        "id": sensor_id,
                        "location_id": location_id,
                        "sensor_type": sensor_type,
                        "manufacturer": (sensor_info.get("sensor_type") or {}).get("manufacturer"),
                        "pin": str(sensor_info.get("pin")) if sensor_info.get("pin") is not None else None,
                        "updated_at": datetime.now(timezone.utc),
                    },
                    [Sensor.id],
                    {
                        "sensor_type": sensor_type,
                        "updated_at": datetime.now(timezone.utc),
                    },
                )
            )

            values = extract_values(item.get("sensordatavalues", []))
            measured_at = parse_timestamp(item["timestamp"]).replace(tzinfo=timezone.utc)

            await session.execute(
                _upsert_stmt(
                    Measurement,
                    {
                        "id": item["id"],
                        "sensor_id": sensor_id,
                        "location_id": location_id,
                        "measured_at": measured_at,
                        "pm10": values["pm10"],
                        "pm25": values["pm25"],
                        "pm1": values["pm1"],
                        "temperature": values["temperature"],
                        "humidity": values["humidity"],
                        "pressure": values["pressure"],
                        "synced_at": datetime.now(timezone.utc),
                    },
                    [Measurement.id],
                )
            )
            saved += 1

        log.records_saved = saved
        log.status = "success"
        log.finished_at = datetime.now(timezone.utc)
    except Exception as exc:
        log.status = "error"
        log.error_message = str(exc)
        log.finished_at = datetime.now(timezone.utc)
        raise
    finally:
        await session.commit()

    return log
