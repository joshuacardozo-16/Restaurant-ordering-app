from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import requests


@dataclass
class DistanceResult:
    ok: bool
    distance_km: Optional[float] = None
    duration_text: Optional[str] = None
    error: Optional[str] = None


def get_distance_and_eta_km(api_key: str, origin: str, destination: str) -> DistanceResult:
    if not api_key:
        return DistanceResult(ok=False, error="Missing GOOGLE_MAPS_API_KEY")

    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origin,
        "destinations": destination,
        "mode": "driving",
        "language": "en-GB",
        "region": "uk",
        "units": "metric",
        "key": api_key,
    }

    try:
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        data = r.json() or {}

        if data.get("status") != "OK":
            return DistanceResult(ok=False, error=f"API status={data.get('status')}")

        rows = data.get("rows") or []
        if not rows or not rows[0].get("elements"):
            return DistanceResult(ok=False, error="No rows/elements")

        el = rows[0]["elements"][0]
        if el.get("status") != "OK":
            return DistanceResult(ok=False, error=f"Element status={el.get('status')}")

        meters = (el.get("distance") or {}).get("value")
        duration_text = (el.get("duration") or {}).get("text")

        if meters is None:
            return DistanceResult(ok=False, error="No distance value")

        km = float(meters) / 1000.0
        return DistanceResult(ok=True, distance_km=km, duration_text=duration_text)

    except Exception as e:
        return DistanceResult(ok=False, error=str(e))
