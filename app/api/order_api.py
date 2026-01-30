from flask import jsonify
from flask_login import login_required, current_user

from . import api_bp
from ..models.order import Order
from ..models.order_item import OrderItem


def _money(val) -> str:
    try:
        return f"{val:.2f}"
    except Exception:
        return str(val)


def _order_item_dict(oi: OrderItem) -> dict:
    return {
        "id": oi.id,
        "menu_item_id": oi.menu_item_id,
        "menu_item_name": oi.menu_item.name if oi.menu_item else None,
        "quantity": oi.quantity,
        "unit_price_at_time": _money(oi.unit_price_at_time),
        "line_total": _money(oi.line_total),
    }


def _order_dict(o: Order) -> dict:
    return {
        "id": o.id,
        "order_type": o.order_type,
        "status": o.status,
        "total_price": _money(o.total_price),
        "created_at": o.created_at.isoformat() if o.created_at else None,
    }


@api_bp.get("/orders")
@login_required
def api_orders_list():
    orders = (
        Order.query
        .filter_by(user_id=current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )
    return jsonify({
        "count": len(orders),
        "orders": [_order_dict(o) for o in orders],
    })


@api_bp.get("/orders/<int:order_id>")
@login_required
def api_orders_detail(order_id: int):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    items = OrderItem.query.filter_by(order_id=order.id).all()

    return jsonify({
        "order": _order_dict(order),
        "items": [_order_item_dict(oi) for oi in items],
    })
