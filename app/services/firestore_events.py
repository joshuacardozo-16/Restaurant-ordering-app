from datetime import datetime, timezone
from google.cloud import firestore

_client = None


def _get_client():
    """
    Lazy Firestore client.
    Uses GOOGLE_APPLICATION_CREDENTIALS locally, default credentials on GCP.
    """
    global _client
    if _client is None:
        _client = firestore.Client()
    return _client


def log_event(event_type: str, payload: dict | None = None):
    """
    Fire-and-forget analytics logging.
    Never breaks the app if Firestore fails.
    """
    try:
        client = _get_client()
        doc = {
            "event_type": event_type,
            "ts": datetime.now(timezone.utc),
            "payload": payload or {},
        }
        client.collection("events").add(doc)
    except Exception:
        # swallow errors so your app still runs
        return
