from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

from ..extensions import db
from ..models.order import Order
from ..models.menu_item import MenuItem
from ..services.authz import admin_required
from .menu_forms import MenuItemForm

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.get("/")
@login_required
@admin_required
def dashboard():
    return render_template("admin/dashboard.html")


@admin_bp.get("/menu")
@login_required
@admin_required
def menu_list():
    items = MenuItem.query.order_by(MenuItem.category.asc(), MenuItem.name.asc()).all()
    return render_template("admin/menu_list.html", items=items)


@admin_bp.route("/menu/new", methods=["GET", "POST"])
@login_required
@admin_required
def menu_new():
    form = MenuItemForm()
    if form.validate_on_submit():
        item = MenuItem(
            name=form.name.data.strip(),
            description=form.description.data.strip() if form.description.data else None,
            price=form.price.data,
            category=form.category.data.strip(),
            image_url=form.image_url.data.strip() if form.image_url.data else None,
            is_available=form.is_available.data,
        )
        db.session.add(item)
        db.session.commit()
        flash("Menu item created ✅", "success")
        return redirect(url_for("admin.menu_list"))
    return render_template("admin/menu_form.html", form=form, mode="new")


@admin_bp.route("/menu/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def menu_edit(item_id: int):
    item = MenuItem.query.get_or_404(item_id)
    form = MenuItemForm(obj=item)
    if form.validate_on_submit():
        item.name = form.name.data.strip()
        item.description = form.description.data.strip() if form.description.data else None
        item.price = form.price.data
        item.category = form.category.data.strip()
        item.image_url = form.image_url.data.strip() if form.image_url.data else None
        item.is_available = form.is_available.data
        db.session.commit()
        flash("Menu item updated ✅", "success")
        return redirect(url_for("admin.menu_list"))
    return render_template("admin/menu_form.html", form=form, mode="edit", item=item)


@admin_bp.post("/menu/<int:item_id>/toggle")
@login_required
@admin_required
def menu_toggle(item_id: int):
    item = MenuItem.query.get_or_404(item_id)
    item.is_available = not item.is_available
    db.session.commit()
    flash("Availability updated ✅", "info")
    return redirect(url_for("admin.menu_list"))


# -----------------------
# Orders management
# -----------------------

@admin_bp.get("/orders")
@login_required
@admin_required
def orders_list():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template("admin/orders.html", orders=orders)


@admin_bp.post("/orders/<int:order_id>/status")
@login_required
@admin_required
def order_update_status(order_id: int):
    order = Order.query.get_or_404(order_id)

    new_status = (request.form.get("status") or "").strip().lower()
    allowed = {"pending", "preparing", "ready", "out_for_delivery", "delivered", "cancelled"}

    if new_status not in allowed:
        flash("Invalid status.", "danger")
        return redirect(url_for("admin.orders_list"))

    order.status = new_status
    db.session.commit()

    flash(f"Order #{order.id} updated to {new_status.replace('_',' ')} ✅", "success")
    return redirect(url_for("admin.orders_list"))
