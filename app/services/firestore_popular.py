from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone
import os

from google.cloud import firestore


# tiny in-memory cache so menu page stays fast
_CACHE = {"ts": None, "popular_ids": set()}


def get_popular_item_ids(days: int = 7, top_n: int = 6, max_scan: int = 2000) -> set[int]:
    """
    Returns a set of menu_item_ids considered 'popular' based on add_to_cart events.
    - Reads from Firestore (NoSQL analytics)
    - Uses caching to keep UI snappy
    - Never breaks the app if Firestore is unavailable
    """
    debug = os.getenv("FIRESTORE_DEBUG") == "1"

    try:
        now = datetime.now(timezone.utc)

        # 60s cache
        if _CACHE["ts"] and (now - _CACHE["ts"]).total_seconds() < 60:
            return _CACHE["popular_ids"]

        client = firestore.Client()  # uses auth default project
        cutoff = now - timedelta(days=days)

        docs = (
            client.collection("events")
            .order_by("ts", direction=firestore.Query.DESCENDING)
            .limit(max_scan)
            .stream()
        )

        counts = Counter()
        seen_add = 0

        for d in docs:
            ev = d.to_dict() or {}

            ev_type = str(ev.get("event_type", "")).strip().lower()
            if ev_type != "add_to_cart":
                continue
            seen_add += 1

            ts = ev.get("ts")
            if ts is None:
                continue

            # Firestore often returns DatetimeWithNanoseconds (still works like datetime)
            if isinstance(ts, datetime):
                if ts.tzinfo is None:
                    ts = ts.replace(tzinfo=timezone.utc)
            else:
                # If it isn't a datetime for some reason, skip safely
                continue

            if ts < cutoff:
                continue

            payload = ev.get("payload") or {}

            # support both keys (just in case)
            item_id = payload.get("item_id", payload.get("menu_item_id"))
            qty = payload.get("qty") or 1

            if item_id is None:
                continue

            try:
                counts[int(item_id)] += int(qty)
            except Exception:
                continue

        popular = {item_id for item_id, _ in counts.most_common(top_n)}

        _CACHE["ts"] = now
        _CACHE["popular_ids"] = popular

        if debug:
            print(f"[popular] scanned={max_scan} add_to_cart_seen={seen_add} popular={popular}")

        return popular

    except Exception as e:
        if debug:
            print("[popular] Firestore popular failed:", e)
        # if Firestore fails, just show no 'popular' badge
        return set()
