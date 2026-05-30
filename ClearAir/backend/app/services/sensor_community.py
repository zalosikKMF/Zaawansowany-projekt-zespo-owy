from datetime import datetime
from typing import Any

import httpx

from app.config import settings


def _parse_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def extract_values(sensordatavalues: list[dict]) -> dict[str, float | None]:
    out: dict[str, float | None] = {
        "pm10": None,
        "pm25": None,
        "pm1": None,
        "temperature": None,
        "humidity": None,
        "pressure": None,
    }
    mapping = {
        "P1": "pm10",
        "P2": "pm25",
        "P0": "pm1",
        "temperature": "temperature",
        "humidity": "humidity",
        "pressure": "pressure",
    }
    for item in sensordatavalues or []:
        vt = item.get("value_type")
        key = mapping.get(vt)
        if key:
            out[key] = _parse_float(item.get("value"))
    return out


def parse_timestamp(ts: str) -> datetime:
    return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")


async def fetch_country_measurements(country: str | None = None) -> list[dict]:
    country = country or settings.sync_country
    url = f"{settings.sensor_community_url}/airrohr/v1/filter/country={country}"
    headers = {"User-Agent": settings.user_agent}
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
