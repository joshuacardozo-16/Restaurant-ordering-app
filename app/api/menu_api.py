from flask import jsonify, request
from sqlalchemy import case

from . import api_bp
from ..models.menu_item import MenuItem


def _menu_item_dict(mi: MenuItem) -> dict:
    return {
        "id": mi.id,
        "name": mi.name,
        "category": mi.category,
        "description": mi.description,
        "price": f"{mi.price:.2f}" if mi.price is not None else "0.00",
        "image_url": mi.image_url,
        "is_available": bool(mi.is_available),
    }


@api_bp.get("/menu")
def api_menu_list():
    q = (request.args.get("q") or "").strip()
    category = (request.args.get("category") or "").strip()

    query = MenuItem.query.filter_by(is_available=True)

    if category:
        query = query.filter(MenuItem.category == category)

    if q:
        query = query.filter(MenuItem.name.ilike(f"%{q}%"))

    # same category order as your UI (optional but nice)
    CATEGORY_ORDER = [
        "Starters", "Sharers", "Mains", "Burgers", "Wraps", "Rice Combos", "Kids Meals",
        "Sides", "Sauces", "Desserts", "Drinks", "Meal Deals",
    ]
    order_case = case(
        {name: i for i, name in enumerate(CATEGORY_ORDER)},
        value=MenuItem.category,
        else_=999,
    )

    items = query.order_by(order_case.asc(), MenuItem.name.asc()).all()

    return jsonify({
        "count": len(items),
        "items": [_menu_item_dict(mi) for mi in items],
    })


@api_bp.get("/menu/<int:item_id>")
def api_menu_detail(item_id: int):
    mi = MenuItem.query.get_or_404(item_id)
    return jsonify(_menu_item_dict(mi))
