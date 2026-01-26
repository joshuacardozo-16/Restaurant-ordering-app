from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any

from google.cloud import firestore

from ..models.order import Order
from ..extensions import db


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _safe_dt(ts: Any) -> datetime | None:
    """
    Firestore returns timestamps as datetime. This helper normalizes and guards.
    """
    if ts is None:
        return None
    if isinstance(ts, datetime):
        # make timezone-aware
        return ts if ts.tzinfo else ts.replace(tzinfo=timezone.utc)
    return None


def fetch_events(days: int = 30, limit: int = 5000) -> list[dict]:
    """
    Pull recent events from Firestore.
    Keeps it simple and avoids needing complex indexes.
    """
    client = firestore.Client()
    cutoff = _utc_now() - timedelta(days=days)

    # Order by ts desc and limit; then filter in Python for safety.
    # This usually avoids Firestore composite index issues.
    docs = (
        client.collection("events")
        .order_by("ts", direction=firestore.Query.DESCENDING)
        .limit(limit)
        .stream()
    )

    events: list[dict] = []
    for d in docs:
        data = d.to_dict() or {}
        ts = _safe_dt(data.get("ts"))
        if ts and ts >= cutoff:
            events.append(data)

    return events


def build_admin_kpis(days: int = 30) -> dict:
    """
    Returns a dict of analytics for dashboard:
    - SQL revenue/orders KPIs
    - Firestore funnel + popular items
    """
    # ---------- SQL KPIs ----------
    cutoff = _utc_now() - timedelta(days=days)

    recent_orders = (
        Order.query
        .filter(Order.created_at >= cutoff.replace(tzinfo=None))  # SQLite naive datetimes
        .order_by(Order.created_at.desc())
        .all()
    )

    total_orders = len(recent_orders)
    revenue = Decimal("0.00")
    for o in recent_orders:
        try:
            revenue += Decimal(str(o.total_price or 0))
        except Exception:
            pass

    avg_order_value = (revenue / total_orders) if total_orders else Decimal("0.00")

    # ---------- Firestore KPIs ----------
    try:
        events = fetch_events(days=days)
        fs_ok = True
    except Exception as e:
        events = []
        fs_ok = False

    by_type = Counter()
    add_item_counts = Counter()
    hour_counts = Counter()

    for ev in events:
        et = (ev.get("event_type") or "").strip()
        by_type[et] += 1

        payload = ev.get("payload") or {}
        # popular items from add_to_cart payload
        if et == "add_to_cart":
            name = payload.get("item_name") or payload.get("name") or payload.get("item") or "Unknown item"
            add_item_counts[str(name)] += int(payload.get("qty") or 1)

        ts = _safe_dt(ev.get("ts"))
        if ts:
            hour_counts[ts.hour] += 1

    menu_views = by_type.get("menu_view", 0)
    add_to_cart = by_type.get("add_to_cart", 0)
    checkout_views = by_type.get("checkout_view", 0)
    order_placed = by_type.get("order_placed", 0)

    # Funnel conversion (guard division)
    def rate(a: int, b: int) -> float:
        return (a / b * 100.0) if b else 0.0

    funnel = {
        "menu_to_cart": rate(add_to_cart, menu_views),
        "cart_to_checkout": rate(checkout_views, add_to_cart),
        "checkout_to_order": rate(order_placed, checkout_views),
        "menu_to_order": rate(order_placed, menu_views),
    }

    top_items = add_item_counts.most_common(10)

    # Peak hour (simple)
    peak_hour = None
    if hour_counts:
        peak_hour = max(hour_counts.items(), key=lambda x: x[1])[0]

    return {
        "days": days,

        # SQL
        "total_orders": total_orders,
        "revenue": revenue,
        "avg_order_value": avg_order_value,
        "recent_orders": recent_orders[:10],

        # Firestore
        "firestore_ok": fs_ok,
        "event_counts": dict(by_type),
        "funnel": funnel,
        "top_items": top_items,
        "peak_hour": peak_hour,
    }
