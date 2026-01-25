from decimal import Decimal
from ..extensions import db
from ..models.order import Order
from ..models.order_item import OrderItem
from .checkout_forms import CheckoutForm
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..services.cart import set_qty

from ..models.menu_item import MenuItem
from ..services.cart import add_to_cart, get_cart, remove_from_cart, clear_cart

customer_bp = Blueprint("customer", __name__, url_prefix="")

@customer_bp.get("/menu")
def menu():
    q = (request.args.get("q") or "").strip()
    category = (request.args.get("category") or "").strip()

    query = MenuItem.query.filter_by(is_available=True)

    if category:
        query = query.filter(MenuItem.category == category)

    if q:
        query = query.filter(MenuItem.name.ilike(f"%{q}%"))

    items = query.order_by(MenuItem.category.asc(), MenuItem.name.asc()).all()

    categories = [
        c[0]
        for c in MenuItem.query.with_entities(MenuItem.category)
        .distinct()
        .order_by(MenuItem.category.asc())
        .all()
    ]

    return render_template(
        "customer/menu.html",
        items=items,
        categories=categories,
        q=q,
        category=category,
    )

@customer_bp.post("/cart/add/<int:item_id>")
@login_required
def cart_add(item_id: int):
    add_to_cart(item_id, 1)
    flash("Added to cart ✅", "success")
    return redirect(request.referrer or url_for("customer.menu"))

@customer_bp.get("/cart")
@login_required
def cart_view():
    cart = get_cart()
    if not cart:
        return render_template("customer/cart.html", items=[], total=0)

    ids = [int(k) for k in cart.keys()]
    menu_items = MenuItem.query.filter(MenuItem.id.in_(ids)).all()

    items = []
    total = 0
    for mi in menu_items:
        qty = int(cart.get(str(mi.id), 0))
        line_total = float(mi.price) * qty
        total += line_total
        items.append({"item": mi, "qty": qty, "line_total": line_total})

    return render_template("customer/cart.html", items=items, total=total)

@customer_bp.post("/cart/remove/<int:item_id>")
@login_required
def cart_remove(item_id: int):
    remove_from_cart(item_id)
    flash("Removed from cart.", "info")
    return redirect(url_for("customer.cart_view"))

@customer_bp.post("/cart/clear")
@login_required
def cart_clear():
    clear_cart()
    flash("Cart cleared.", "info")
    return redirect(url_for("customer.cart_view"))

@customer_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    cart = get_cart()
    if not cart:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("customer.menu"))

    # Build cart summary from DB
    ids = [int(k) for k in cart.keys()]
    menu_items = MenuItem.query.filter(MenuItem.id.in_(ids), MenuItem.is_available == True).all()  # noqa: E712
    if not menu_items:
        flash("No available items found in your cart.", "warning")
        return redirect(url_for("customer.menu"))

    cart_rows = []
    total = Decimal("0.00")
    for mi in menu_items:
        qty = int(cart.get(str(mi.id), 0))
        if qty <= 0:
            continue
        line_total = (Decimal(str(mi.price)) * qty)
        total += line_total
        cart_rows.append({"item": mi, "qty": qty, "line_total": line_total})

    form = CheckoutForm()

    if form.validate_on_submit():
        order_type = form.order_type.data

        # Validate required fields based on order_type
        if order_type == "delivery":
            if not form.delivery_address_line1.data or not form.city.data or not form.postcode.data:
                flash("For delivery, please provide Address line 1, City and Postcode.", "danger")
                return render_template("customer/checkout.html", form=form, cart_rows=cart_rows, total=total)
        else:  # pickup
            if not form.pickup_time_requested.data:
                flash("For pickup, please provide a pickup time.", "danger")
                return render_template("customer/checkout.html", form=form, cart_rows=cart_rows, total=total)

        # Create Order
        order = Order(
            user_id=current_user.id,
            order_type=order_type,
            status="pending",
            total_price=total,
            delivery_address_line1=form.delivery_address_line1.data.strip() if form.delivery_address_line1.data else None,
            delivery_address_line2=form.delivery_address_line2.data.strip() if form.delivery_address_line2.data else None,
            city=form.city.data.strip() if form.city.data else None,
            postcode=form.postcode.data.strip() if form.postcode.data else None,
            delivery_instructions=form.delivery_instructions.data.strip() if form.delivery_instructions.data else None,
            pickup_time_requested=form.pickup_time_requested.data.strip() if form.pickup_time_requested.data else None,
        )
        db.session.add(order)
        db.session.flush()  # gives order.id without committing yet

        # Create OrderItems
        for row in cart_rows:
            mi = row["item"]
            qty = int(row["qty"])
            unit_price = Decimal(str(mi.price))
            oi = OrderItem(
                order_id=order.id,
                menu_item_id=mi.id,
                quantity=qty,
                unit_price_at_time=unit_price,
                line_total=unit_price * qty,
            )
            db.session.add(oi)

        # Recalculate total from items (extra safety)
        db.session.flush()
        order.recalc_total()

        db.session.commit()
        clear_cart()

        flash("Order placed successfully ✅", "success")
        return redirect(url_for("customer.order_confirmation", order_id=order.id))

    return render_template("customer/checkout.html", form=form, cart_rows=cart_rows, total=total)


@customer_bp.get("/orders/<int:order_id>")
@login_required
def order_confirmation(order_id: int):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    return render_template("customer/order_confirmation.html", order=order)


@customer_bp.get("/my-orders")
@login_required
def my_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template("customer/my_orders.html", orders=orders)

@customer_bp.post("/cart/inc/<int:item_id>")
@login_required
def cart_inc(item_id: int):
    cart = get_cart()
    current = int(cart.get(str(item_id), 0))
    set_qty(item_id, current + 1)
    return redirect(url_for("customer.cart_view"))

@customer_bp.post("/cart/dec/<int:item_id>")
@login_required
def cart_dec(item_id: int):
    cart = get_cart()
    current = int(cart.get(str(item_id), 0))
    set_qty(item_id, current - 1)
    return redirect(url_for("customer.cart_view"))
