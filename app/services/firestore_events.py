from __future__ import annotations

from datetime import datetime, timezone
from threading import Thread
from typing import Optional

from google.cloud import firestore

_client: Optional[firestore.Client] = None


def _get_client() -> firestore.Client:
    """
    Lazy Firestore client.
    Only created when needed, so the app never crashes on startup.
    """
    global _client
    if _client is None:
        _client = firestore.Client()  # uses GOOGLE_APPLICATION_CREDENTIALS / ADC
    return _client


def _write_event(event_type: str, payload: dict):
    """
    Runs in a background thread so requests stay fast.
    """
    try:
        client = _get_client()
        client.collection("events").add(
            {
                "event_type": event_type,
                "ts": datetime.now(timezone.utc),
                "payload": payload or {},
            }
        )
    except Exception:
        # Never break the app for analytics
        return


def log_event(event_type: str, payload: dict | None = None):
    """
    Fire-and-forget analytics logging (non-blocking).
    """
    Thread(target=_write_event, args=(event_type, payload or {}), daemon=True).start()
