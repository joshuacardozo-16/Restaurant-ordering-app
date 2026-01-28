from __future__ import annotations
from datetime import datetime, timezone
from ..extensions import db


class LoyaltyAccount(db.Model):
    __tablename__ = "loyalty_accounts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)

    points_balance = db.Column(db.Integer, nullable=False, default=0)
    lifetime_earned = db.Column(db.Integer, nullable=False, default=0)
    lifetime_redeemed = db.Column(db.Integer, nullable=False, default=0)

    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class LoyaltyTransaction(db.Model):
    """
    NOTE: This matches your EXISTING sqlite table:
      id, user_id, order_id, kind, points, ts, note
    """
    __tablename__ = "loyalty_transactions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # optional link to order
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=True)

    # "earn" or "redeem"
    kind = db.Column(db.String(32), nullable=False)

    # positive integer points
    points = db.Column(db.Integer, nullable=False)

    ts = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    # optional human note
    note = db.Column(db.String(200), nullable=True)
