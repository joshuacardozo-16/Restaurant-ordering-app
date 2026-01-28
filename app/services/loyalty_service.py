from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal

from ..extensions import db
from ..models.loyalty import LoyaltyAccount, LoyaltyTransaction


def _utcnow():
    return datetime.now(timezone.utc)


def _get_or_create_account(user_id: int) -> LoyaltyAccount:
    acct = LoyaltyAccount.query.filter_by(user_id=user_id).first()
    if acct:
        return acct

    acct = LoyaltyAccount(
        user_id=user_id,
        points_balance=0,
        lifetime_earned=0,
        lifetime_redeemed=0,
        created_at=_utcnow(),
        updated_at=_utcnow(),
    )
    db.session.add(acct)
    return acct


def award_points_for_order(user_id: int, order_id: int, order_total: Decimal) -> int:
    """
    Long-term loyalty rule:
    - 1 point per £1 spent (rounded down)
    - Minimum 5 points per order
    """
    pounds = int(order_total)  # floor
    points = max(5, pounds)

    acct = _get_or_create_account(user_id)
    acct.points_balance += points
    acct.lifetime_earned += points
    acct.updated_at = datetime.now(timezone.utc)

    tx = LoyaltyTransaction(
        user_id=user_id,
        order_id=order_id,
        kind="earn",
        points=points,
        note=f"Earned from order #{order_id}",
    )
    db.session.add(tx)

    return points


def redeem_points(user_id: int, points_cost: int, note: str) -> bool:
    acct = _get_or_create_account(user_id)

    if acct.points_balance < points_cost:
        return False

    acct.points_balance -= points_cost
    acct.lifetime_redeemed += points_cost
    acct.updated_at = _utcnow()

    tx = LoyaltyTransaction(
        user_id=user_id,
        order_id=None,
        kind="redeem",
        points=points_cost,
        ts=_utcnow(),
        note=note,
    )
    db.session.add(tx)

    return True


def award_welcome_bonus_if_first_time(user_id: int, bonus_points: int = 50) -> bool:
    """
    Welcome bonus only once.
    Uses existing DB schema:
    - kind / points / ts / note
    """
    exists = LoyaltyTransaction.query.filter_by(user_id=user_id, kind="welcome").first()
    if exists:
        return False

    acct = _get_or_create_account(user_id)
    acct.points_balance += bonus_points
    acct.lifetime_earned += bonus_points
    acct.updated_at = _utcnow()

    tx = LoyaltyTransaction(
        user_id=user_id,
        order_id=None,
        kind="welcome",
        points=bonus_points,
        ts=_utcnow(),
        note="Welcome bonus",
    )
    db.session.add(tx)

    return True
