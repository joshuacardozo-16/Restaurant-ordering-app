from flask import jsonify, request, abort
from flask_login import login_required, current_user

from . import api_bp
from ..extensions import db
from ..models.menu_item import MenuItem


def _require_admin():
    if not current_user.is_authenticated:
        abort(401)
    if getattr(current_user, "role", None) != "admin":
        abort(403)


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


@api_bp.get("/admin/menu")
@login_required
def admin_menu_list():
    _require_admin()
    items = MenuItem.query.order_by(MenuItem.id.desc()).all()
    return jsonify({"count": len(items), "items": [_menu_item_dict(mi) for mi in items]})


@api_bp.post("/admin/menu")
@login_required
def admin_menu_create():
    _require_admin()

    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    category = (data.get("category") or "").strip()
    price = data.get("price")

    if not name or not category or price is None:
        return jsonify({"error": "name, category, price are required"}), 400

    mi = MenuItem(
        name=name,
        category=category,
        description=(data.get("description") or "").strip() or None,
        price=price,
        image_url=(data.get("image_url") or "").strip() or None,
        is_available=bool(data.get("is_available", True)),
    )
    db.session.add(mi)
    db.session.commit()
    return jsonify({"created": _menu_item_dict(mi)}), 201


@api_bp.put("/admin/menu/<int:item_id>")
@login_required
def admin_menu_update(item_id: int):
    _require_admin()

    mi = MenuItem.query.get_or_404(item_id)
    data = request.get_json(silent=True) or {}

    if "name" in data:
        mi.name = (data["name"] or "").strip()
    if "category" in data:
        mi.category = (data["category"] or "").strip()
    if "description" in data:
        mi.description = (data["description"] or "").strip() or None
    if "price" in data:
        mi.price = data["price"]
    if "image_url" in data:
        mi.image_url = (data["image_url"] or "").strip() or None
    if "is_available" in data:
        mi.is_available = bool(data["is_available"])

    db.session.commit()
    return jsonify({"updated": _menu_item_dict(mi)})


@api_bp.delete("/admin/menu/<int:item_id>")
@login_required
def admin_menu_delete(item_id: int):
    _require_admin()

    mi = MenuItem.query.get_or_404(item_id)
    db.session.delete(mi)
    db.session.commit()
    return jsonify({"deleted_id": item_id})
