from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy import case  # for custom category order

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
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
from ..services.firestore_events import log_event  # analytics
from ..services.firestore_popular import get_popular_item_ids  # popular badge
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

def get_menu_recommendations(cart: dict, popular_ids: set[int], limit: int = 8):
    """
    Menu page recommendations:
    - If user has items in cart -> upsell add-ons (sides/sauces/drinks/desserts)
    - Else -> show popular items (Firestore), fallback to some available items
    """
    cart_ids = {int(k) for k in cart.keys()} if cart else set()

    # If cart has a main item, upsell add-ons
    main_categories = {"mains", "burgers", "wraps", "rice combos"}
    upsell_categories = ["Sides", "Sauces", "Drinks", "Desserts"]

    if cart_ids:
        cart_items = MenuItem.query.filter(MenuItem.id.in_(list(cart_ids))).all()
        has_main = any(((it.category or "").strip().lower() in main_categories) for it in cart_items)

        if has_main:
            return (
                MenuItem.query
                .filter(MenuItem.is_available == True)  # noqa: E712
                .filter(MenuItem.category.in_(upsell_categories))
                .filter(~MenuItem.id.in_(list(cart_ids)))
                .order_by(MenuItem.category.asc(), MenuItem.price.asc())
                .limit(limit)
                .all()
            )

    # Otherwise show popular items first (not in cart)
    if popular_ids:
        recs = (
            MenuItem.query
            .filter(MenuItem.is_available == True)  # noqa: E712
            .filter(MenuItem.id.in_(list(popular_ids)))
            .filter(~MenuItem.id.in_(list(cart_ids)))
            .limit(limit)
            .all()
        )
        if recs:
            return recs

    # Fallback: cheapest/featured items (not in cart)
    return (
        MenuItem.query
        .filter(MenuItem.is_available == True)  # noqa: E712
        .filter(~MenuItem.id.in_(list(cart_ids)))
        .order_by(MenuItem.price.asc())
        .limit(limit)
        .all()
    )

@customer_bp.get("/menu")
def menu():
    q = (request.args.get("q") or "").strip()
    category = (request.args.get("category") or "").strip()

    query = MenuItem.query.filter_by(is_available=True)

    if category:
        query = query.filter(MenuItem.category == category)

    if q:
        query = query.filter(MenuItem.name.ilike(f"%{q}%"))

    # Custom category order
    CATEGORY_ORDER = [
        "Starters",
        "Sharers",
        "Mains",
        "Burgers",
        "Wraps",
        "Rice Combos",
        "Kids Meals",
        "Sides",
        "Sauces",
        "Desserts",
        "Drinks",
        "Meal Deals",
    ]

    order_case = case(
        {name: i for i, name in enumerate(CATEGORY_ORDER)},
        value=MenuItem.category,
        else_=999,
    )

    items = query.order_by(order_case.asc(), MenuItem.name.asc()).all()

    categories = [
        c[0]
        for c in MenuItem.query.with_entities(MenuItem.category)
        .distinct()
        .order_by(order_case.asc())
        .all()
    ]

    # Popular (Firestore)
    popular_ids = get_popular_item_ids(days=30, top_n=6)

    # Fallback popular if Firestore has no add_to_cart events yet
    if not popular_ids:
        fallback_items = (
            MenuItem.query.filter_by(is_available=True)
            .order_by(MenuItem.price.desc())
            .limit(6)
            .all()
        )
        popular_ids = {m.id for m in fallback_items}

    cart = get_cart() if current_user.is_authenticated else {}
    menu_recs = get_menu_recommendations(cart, popular_ids, limit=8)


    # Analytics (async)
    log_event(
        "menu_view",
        {
            "q": q or None,
            "category": category or None,
            "user_id": current_user.id if current_user.is_authenticated else None,
        },
    )

    return render_template(
        "customer/menu.html",
        items=items,
        categories=categories,
        q=q,
        category=category,
        popular_ids=popular_ids,
        menu_recs=menu_recs,
    )


# ----------------------------
# Meal Deal chooser (ONE flow)
# ----------------------------

@customer_bp.get("/meal-deal/<int:deal_id>/choose")
@login_required
def meal_deal_choose(deal_id: int):
    deal = MenuItem.query.get_or_404(deal_id)

    if (deal.category or "").strip().lower() not in {"meal deals", "meal deal"}:
        abort(404)

    burgers = (
        MenuItem.query
        .filter(MenuItem.is_available == True)  # noqa: E712
        .filter(MenuItem.category == "Burgers")
        .order_by(MenuItem.name.asc())
        .all()
    )

    sides = (
        MenuItem.query
        .filter(MenuItem.is_available == True)  # noqa: E712
        .filter(MenuItem.category == "Sides")
        .order_by(MenuItem.name.asc())
        .all()
    )

    drinks = (
        MenuItem.query
        .filter(MenuItem.is_available == True)  # noqa: E712
        .filter(MenuItem.category == "Drinks")
        .order_by(MenuItem.name.asc())
        .all()
    )

    return render_template(
        "customer/meal_deal_choose.html",
        deal=deal,
        burgers=burgers,
        sides=sides,
        drinks=drinks,
    )


@customer_bp.post("/meal-deal/<int:deal_id>/choose")
@login_required
def meal_deal_choose_post(deal_id: int):
    deal = MenuItem.query.get_or_404(deal_id)

    # Only allow for "Meal Deals"
    if (deal.category or "").strip().lower() not in {"meal deals", "meal deal"}:
        abort(404)

    try:
        burger_id = int(request.form.get("burger_id", "0"))
        side_id = int(request.form.get("side_id", "0"))
        drink_id = int(request.form.get("drink_id", "0"))
    except ValueError:
        flash("Please choose a burger, side, and drink.", "danger")
        return redirect(url_for("customer.meal_deal_choose", deal_id=deal_id))

    if not burger_id or not side_id or not drink_id:
        flash("Please select a burger, a side, and a drink.", "danger")
        return redirect(url_for("customer.meal_deal_choose", deal_id=deal_id))

    # Validate selected items exist + are available
    selected = MenuItem.query.filter(MenuItem.id.in_([burger_id, side_id, drink_id])).all()
    selected_ids = {m.id for m in selected}

    if burger_id not in selected_ids or side_id not in selected_ids or drink_id not in selected_ids:
        flash("Invalid selection. Please try again.", "danger")
        return redirect(url_for("customer.meal_deal_choose", deal_id=deal_id))

    if not all(m.is_available for m in selected):
        flash("One of your selected items is not available.", "danger")
        return redirect(url_for("customer.meal_deal_choose", deal_id=deal_id))

    # ✅ Save choices into session (so cart can display bundle)
    meal_choices = session.get("meal_deal_choices", {}) or {}
    meal_choices[str(deal_id)] = {
        "burger_id": burger_id,
        "side_id": side_id,
        "drink_id": drink_id,
    }
    session["meal_deal_choices"] = meal_choices
    session.modified = True

    # ✅ Add the meal deal item to cart automatically
    add_to_cart(deal_id, 1)

    # ✅ Analytics (optional)
    log_event("meal_deal_selected", {
        "user_id": current_user.id,
        "deal_id": deal_id,
        "burger_id": burger_id,
        "side_id": side_id,
        "drink_id": drink_id,
    })

    flash("Meal deal added to cart ✅", "success")
    return redirect(url_for("customer.cart_view"))

# ----------------------------
# Cart
# ----------------------------

@customer_bp.post("/cart/add/<int:item_id>")
@login_required
def cart_add(item_id: int):
    item = MenuItem.query.get_or_404(item_id)

    # If meal deal: add it, then force chooser
    if (item.category or "").strip().lower() in {"meal deals", "meal deal"}:
        add_to_cart(item_id, 1)
        log_event("add_to_cart", {"user_id": current_user.id, "item_id": item_id, "qty": 1})
        return redirect(url_for("customer.meal_deal_choose", deal_id=item_id))

    add_to_cart(item_id, 1)

    log_event(
        "add_to_cart",
        {
            "user_id": current_user.id,
            "item_id": item_id,
            "qty": 1,
        },
    )

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

    meal_choices = session.get("meal_deal_choices", {}) or {}

    # pull all selected IDs in one query
    selected_ids = set()
    for _, sel in meal_choices.items():
        selected_ids.add(sel.get("burger_id"))
        selected_ids.add(sel.get("side_id"))
        selected_ids.add(sel.get("drink_id"))
    selected_ids = {i for i in selected_ids if isinstance(i, int)}

    selected_lookup = {}
    if selected_ids:
        selected_items = MenuItem.query.filter(MenuItem.id.in_(list(selected_ids))).all()
        selected_lookup = {m.id: m for m in selected_items}

    for mi in menu_items:
        qty = int(cart.get(str(mi.id), 0))
        if qty <= 0:
            continue

        line_total = (Decimal(str(mi.price)) * qty).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        total += line_total

        bundle = None
        if (mi.category or "").strip().lower() in {"meal deals", "meal deal"}:
            sel = meal_choices.get(str(mi.id))
            if sel:
                bundle = {
                    "burger": selected_lookup.get(sel.get("burger_id")),
                    "side": selected_lookup.get(sel.get("side_id")),
                    "drink": selected_lookup.get(sel.get("drink_id")),
                }

        items.append({"item": mi, "qty": qty, "line_total": line_total, "bundle": bundle})

    total = total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    recs = get_recommendations(cart, limit=6)

    return render_template("customer/cart.html", items=items, total=total, recs=recs)


@customer_bp.post("/cart/remove/<int:item_id>")
@login_required
def cart_remove(item_id: int):
    remove_from_cart(item_id)

    # remove meal choices if this item was a deal
    meal_choices = session.get("meal_deal_choices", {}) or {}
    meal_choices.pop(str(item_id), None)
    session["meal_deal_choices"] = meal_choices

    flash("Removed from cart.", "info")
    return redirect(url_for("customer.cart_view"))


@customer_bp.post("/cart/clear")
@login_required
def cart_clear():
    clear_cart()
    session["meal_deal_choices"] = {}
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


# ----------------------------
# Checkout + Orders (unchanged)
# ----------------------------

@customer_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    cart = get_cart()
    if not cart:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("customer.menu"))

    log_event(
        "checkout_view",
        {"user_id": current_user.id, "cart_size": sum(int(v) for v in cart.values())},
    )

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

        discount = Decimal("0.00")
        delivery_fee = Decimal("0.00")

        if order_type == "pickup":
            discount = (subtotal * PICKUP_DISCOUNT_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        else:
            delivery_fee = Decimal("0.00") if subtotal >= FREE_DELIVERY_THRESHOLD else DELIVERY_FEE

        total = (subtotal - discount + delivery_fee).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        pickup_time = None

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
        else:
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

        raw = (form.card_number.data or "").replace(" ", "")
        session["payment_last4"] = raw[-4:] if len(raw) >= 4 else None

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
        db.session.flush()

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
        session["meal_deal_choices"] = {}

        log_event(
            "order_placed",
            {
                "order_id": order.id,
                "user_id": current_user.id,
                "order_type": order_type,
                "subtotal": str(subtotal),
                "discount": str(discount),
                "delivery_fee": str(delivery_fee),
                "total": str(total),
                "items": [{"item_id": r["item"].id, "qty": r["qty"]} for r in cart_rows],
            },
        )

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
