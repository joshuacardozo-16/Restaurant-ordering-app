from decimal import Decimal, ROUND_HALF_UP

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user

from ..extensions import db
from ..models.menu_item import MenuItem
from ..models.order import Order
from ..models.order_item import OrderItem
from ..services.cart import (
    add_to_cart,
    get_cart,
    remove_from_cart,
    clear_cart,
    set_qty,
)
from ..services.firestore_events import log_event  # ✅ NEW
from .checkout_forms import CheckoutForm

customer_bp = Blueprint("customer", __name__, url_prefix="")

DELIVERY_FEE = Decimal("2.99")
FREE_DELIVERY_THRESHOLD = Decimal("25.00")
PICKUP_DISCOUNT_RATE = Decimal("0.15")


def get_recommendations(cart: dict, limit: int = 6):
    """
    Simple upsell engine:
    If cart contains a main category, recommend add-ons (sides/sauces/drinks/desserts)
    not already in the cart.
    """
    if not cart:
        return []

    cart_ids = {int(k) for k in cart.keys()} if cart else set()

    main_categories = {"mains", "burgers", "wraps", "rice combos", "meal deals"}
    upsell_categories = ["Sides", "Sauces", "Drinks", "Desserts"]

    cart_items = MenuItem.query.filter(MenuItem.id.in_(list(cart_ids))).all()
    has_main = any(((it.category or "").strip().lower() in main_categories) for it in cart_items)

    if not has_main:
        return []

    recs = (
        MenuItem.query
        .filter(MenuItem.is_available == True)  # noqa: E712
        .filter(MenuItem.category.in_(upsell_categories))
        .filter(~MenuItem.id.in_(list(cart_ids)))
        .order_by(MenuItem.category.asc(), MenuItem.price.asc())
        .limit(limit)
        .all()
    )
    return recs


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

    # ✅ Analytics
    log_event("menu_view", {
        "q": q or None,
        "category": category or None,
        "user_id": current_user.id if current_user.is_authenticated else None,
    })

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

    # ✅ Analytics
    log_event("add_to_cart", {
        "user_id": current_user.id,
        "item_id": item_id,
        "qty": 1,
    })

    flash("Added to cart ✅", "success")
    return redirect(request.referrer or url_for("customer.menu"))


@customer_bp.get("/cart")
@login_required
def cart_view():
    cart = get_cart()
    if not cart:
        return render_template("customer/cart.html", items=[], total=Decimal("0.00"), recs=[])

    ids = [int(k) for k in cart.keys()]
    menu_items = MenuItem.query.filter(MenuItem.id.in_(ids)).all()

    items = []
    total = Decimal("0.00")
    for mi in menu_items:
        qty = int(cart.get(str(mi.id), 0))
        if qty <= 0:
            continue
        line_total = (Decimal(str(mi.price)) * qty).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        total += line_total
        items.append({"item": mi, "qty": qty, "line_total": line_total})

    total = total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    recs = get_recommendations(cart, limit=6)
    return render_template("customer/cart.html", items=items, total=total, recs=recs)


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


@customer_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    cart = get_cart()
    if not cart:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("customer.menu"))

    # ✅ Analytics
    log_event("checkout_view", {
        "user_id": current_user.id,
        "cart_size": sum(int(v) for v in cart.values()),
    })

    # Load items from DB
    ids = [int(k) for k in cart.keys()]
    menu_items = MenuItem.query.filter(MenuItem.id.in_(ids), MenuItem.is_available == True).all()  # noqa: E712
    if not menu_items:
        flash("No available items found in your cart.", "warning")
        return redirect(url_for("customer.menu"))

    cart_rows = []
    subtotal = Decimal("0.00")

    for mi in menu_items:
        qty = int(cart.get(str(mi.id), 0))
        if qty <= 0:
            continue
        line_total = (Decimal(str(mi.price)) * qty).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        subtotal += line_total
        cart_rows.append({"item": mi, "qty": qty, "line_total": line_total})

    subtotal = subtotal.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    form = CheckoutForm()

    # Compute pricing for initial render (and when user changes order_type via ?order_type=...)
    selected_type = (request.args.get("order_type") or form.order_type.data or "delivery").strip()
    form.order_type.data = selected_type

    discount = Decimal("0.00")
    delivery_fee = Decimal("0.00")

    if selected_type == "pickup":
        discount = (subtotal * PICKUP_DISCOUNT_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    else:
        delivery_fee = Decimal("0.00") if subtotal >= FREE_DELIVERY_THRESHOLD else DELIVERY_FEE

    total = (subtotal - discount + delivery_fee).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    if form.validate_on_submit():
        order_type = (form.order_type.data or "delivery").strip()

        # recompute totals based on submitted choice
        discount = Decimal("0.00")
        delivery_fee = Decimal("0.00")

        if order_type == "pickup":
            discount = (subtotal * PICKUP_DISCOUNT_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        else:
            delivery_fee = Decimal("0.00") if subtotal >= FREE_DELIVERY_THRESHOLD else DELIVERY_FEE

        total = (subtotal - discount + delivery_fee).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # IMPORTANT: define pickup_time for both branches (prevents UnboundLocalError)
        pickup_time = None

        # Validate conditional fields
        if order_type == "delivery":
            addr1 = (form.delivery_address_line1.data or "").strip()
            city = (form.city.data or "").strip()
            postcode = (form.postcode.data or "").strip()

            if not addr1 or not city or not postcode:
                flash("For delivery, please provide Address line 1, City and Postcode.", "danger")
                return render_template(
                    "customer/checkout.html",
                    form=form,
                    cart_rows=cart_rows,
                    subtotal=subtotal,
                    discount=discount,
                    delivery_fee=delivery_fee,
                    total=total,
                )
        else:  # pickup
            pickup_time = (form.pickup_time_requested.data or "").strip()
            if not pickup_time:
                flash("For pickup, please provide a pickup time (e.g. 18:30).", "danger")
                return render_template(
                    "customer/checkout.html",
                    form=form,
                    cart_rows=cart_rows,
                    subtotal=subtotal,
                    discount=discount,
                    delivery_fee=delivery_fee,
                    total=total,
                )

        # Store only safe payment metadata (NEVER store card number or CVC)
        raw = (form.card_number.data or "").replace(" ", "")
        session["payment_last4"] = raw[-4:] if len(raw) >= 4 else None

        # Create Order (total_price includes discount/fee)
        order = Order(
            user_id=current_user.id,
            order_type=order_type,
            status="pending",
            total_price=total,
            delivery_address_line1=(form.delivery_address_line1.data or "").strip() if order_type == "delivery" else None,
            delivery_address_line2=(form.delivery_address_line2.data or "").strip() if order_type == "delivery" else None,
            city=(form.city.data or "").strip() if order_type == "delivery" else None,
            postcode=(form.postcode.data or "").strip() if order_type == "delivery" else None,
            delivery_instructions=(form.delivery_instructions.data or "").strip() if order_type == "delivery" else None,
            pickup_time_requested=pickup_time,
        )
        db.session.add(order)
        db.session.flush()  # get order.id

        # Create OrderItems (line totals are subtotal per item; discount/fee reflected in order.total_price)
        for row in cart_rows:
            mi = row["item"]
            qty = int(row["qty"])
            unit_price = Decimal(str(mi.price)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            oi = OrderItem(
                order_id=order.id,
                menu_item_id=mi.id,
                quantity=qty,
                unit_price_at_time=unit_price,
                line_total=(unit_price * qty).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            )
            db.session.add(oi)

        db.session.commit()
        clear_cart()

        # ✅ Analytics (after successful commit)
        log_event("order_placed", {
            "order_id": order.id,
            "user_id": current_user.id,
            "order_type": order_type,
            "subtotal": str(subtotal),
            "discount": str(discount),
            "delivery_fee": str(delivery_fee),
            "total": str(total),
            "items": [{"item_id": r["item"].id, "qty": r["qty"]} for r in cart_rows],
        })

        flash("Order placed successfully ✅", "success")
        return redirect(url_for("customer.order_confirmation", order_id=order.id))

    return render_template(
        "customer/checkout.html",
        form=form,
        cart_rows=cart_rows,
        subtotal=subtotal,
        discount=discount,
        delivery_fee=delivery_fee,
        total=total,
    )


@customer_bp.get("/orders/<int:order_id>")
@login_required
def order_confirmation(order_id: int):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    last4 = session.pop("payment_last4", None)
    return render_template("customer/order_confirmation.html", order=order, last4=last4)


@customer_bp.get("/my-orders")
@login_required
def my_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template("customer/my_orders.html", orders=orders)
