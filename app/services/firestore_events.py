from datetime import datetime, timezone
from google.cloud import firestore

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = firestore.Client()
    return _client

def log_event(event_type: str, payload: dict | None = None):
    try:
        client = _get_client()
        doc = {
            "event_type": event_type,
            "ts": datetime.now(timezone.utc),
            "payload": payload or {},
        }
        client.collection("events").add(doc)
    except Exception as e:
        print("Firestore logging failed:", e)
