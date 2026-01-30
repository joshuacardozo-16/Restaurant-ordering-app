from decimal import Decimal, ROUND_HALF_UP

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_required, current_user
from sqlalchemy import case
from flask import session
from ..models.order import Order

from ..extensions import db
from ..models.menu_item import MenuItem
from ..models.order import Order
from ..models.order_item import OrderItem
from ..models.loyalty import LoyaltyAccount, LoyaltyTransaction

from ..services.cart import add_to_cart, get_cart, remove_from_cart, clear_cart, set_qty
from ..services.firestore_events import log_event
from ..services.firestore_popular import get_popular_item_ids
from ..services.loyalty_service import award_points_for_order

from .checkout_forms import CheckoutForm

from flask_login import login_required, current_user
from ..models.order import Order

from flask import current_app
from ..services.maps_distance import get_distance_and_eta_km
import re


customer_bp = Blueprint("customer", __name__, url_prefix="")

DELIVERY_FEE = Decimal("2.99")
FREE_DELIVERY_THRESHOLD = Decimal("25.00")
PICKUP_DISCOUNT_RATE = Decimal("0.15")

NEW_CUSTOMER_MIN_SPEND = Decimal("15.00")
NEW_CUSTOMER_RATE = Decimal("0.10")   # 10%
NEW_CUSTOMER_CAP = Decimal("5.00")    # max £5


def is_first_order_eligible(user_id: int) -> bool:
    # first order only + not admin
    if not current_user.is_authenticated:
        return False
    if getattr(current_user, "role", None) == "admin":
        return False

    has_order = db.session.query(Order.id).filter(Order.user_id == user_id).first() is not None
    return not has_order

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


    # ✅ New customer promo banner (show once per session)
    if current_user.is_authenticated and is_first_order_eligible(current_user.id):
    # Only show if they could actually use it (needs paid subtotal >= £15 later)
        if not session.get("shown_new_customer_offer"):
            flash("🎉 Welcome! You get 10% off your first order (up to £5). Minimum spend £15. Not combinable with pickup discount.", "success")
            session["shown_new_customer_offer"] = True
            session.modified = True

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

    # ✅ reward freebies
    free_ids = set(session.get("free_item_ids", []) or [])

    # ✅ meal deal bundles
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

        # ✅ FREE handling
        is_free = mi.id in free_ids
        if is_free:
            line_total = Decimal("0.00")
        else:
            line_total = (Decimal(str(mi.price)) * qty).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            total += line_total

        # ✅ Meal deal bundle display (optional)
        bundle = None
        if (mi.category or "").strip().lower() in {"meal deals", "meal deal"}:
            sel = meal_choices.get(str(mi.id))
            if sel:
                bundle = {
                    "burger": selected_lookup.get(sel.get("burger_id")),
                    "side": selected_lookup.get(sel.get("side_id")),
                    "drink": selected_lookup.get(sel.get("drink_id")),
                }

        items.append({
            "item": mi,
            "qty": qty,
            "line_total": line_total,
            "bundle": bundle,
            "is_free": is_free,
        })

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
# Checkout + Orders (Delivery quote + Checkout)
# ----------------------------

import re
from decimal import Decimal, ROUND_HALF_UP
from wtforms.validators import Optional
from flask import (
    jsonify, request, current_app,
    flash, redirect, url_for, render_template, session
)
from flask_login import login_required, current_user

# Keep this ONE regex only (no duplicates)
UK_POSTCODE_RE = re.compile(r"^[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}$", re.I)


@customer_bp.get("/delivery-quote")
@login_required
def delivery_quote():
    """
    Returns JSON: distance_km, eta, blocked
    Called by checkout page via fetch() as user types postcode.
    """
    postcode = (request.args.get("postcode") or "").strip().upper()
    if not postcode or not UK_POSTCODE_RE.match(postcode):
        return jsonify({"ok": False, "error": "invalid_postcode"}), 200

    origin = current_app.config.get("RESTAURANT_ADDRESS", "Bournemouth, UK")
    api_key = current_app.config.get("GOOGLE_MAPS_API_KEY", "")
    max_km = float(current_app.config.get("DELIVERY_MAX_KM", 5.0))

    if not api_key:
        return jsonify({"ok": False, "error": "missing_api_key"}), 200

    res = get_distance_and_eta_km(api_key=api_key, origin=origin, destination=postcode)
    if not res.ok or res.distance_km is None:
        return jsonify({"ok": False, "error": "maps_failed"}), 200

    blocked = float(res.distance_km) > float(max_km)

    return jsonify({
        "ok": True,
        "postcode": postcode,
        "distance_km": float(res.distance_km),
        "eta": res.duration_text,
        "blocked": bool(blocked),
        "max_km": float(max_km),
    }), 200


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

    free_ids = set(session.get("free_item_ids", []) or [])

    ids = [int(k) for k in cart.keys()]
    menu_items = MenuItem.query.filter(
        MenuItem.id.in_(ids),
        MenuItem.is_available == True  # noqa: E712
    ).all()

    if not menu_items:
        flash("No available items found in your cart.", "warning")
        return redirect(url_for("customer.menu"))

    cart_rows = []
    subtotal = Decimal("0.00")  # paid subtotal only (free items excluded)

    for mi in menu_items:
        qty = int(cart.get(str(mi.id), 0))
        if qty <= 0:
            continue

        is_free = mi.id in free_ids

        if is_free:
            line_total = Decimal("0.00")
        else:
            line_total = (Decimal(str(mi.price)) * qty).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            subtotal += line_total

        cart_rows.append({
            "item": mi,
            "qty": qty,
            "line_total": line_total,
            "is_free": is_free
        })

    subtotal = subtotal.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    form = CheckoutForm()

    selected_type = (request.args.get("order_type") or form.order_type.data or "delivery").strip()
    form.order_type.data = selected_type

    # -----------------------
    # ✅ Maps API delivery radius check (NO refresh needed)
    # - delivery_info used to display distance/ETA
    # - delivery_blocked used to hard-stop on POST
    # -----------------------
    delivery_info = None
    delivery_blocked = False

    if selected_type == "delivery":
        # Prefer POST (normal form submit), else GET
        postcode_guess = (
            (form.postcode.data or "").strip().upper()
            or (request.args.get("postcode") or "").strip().upper()
        )

        if postcode_guess and UK_POSTCODE_RE.match(postcode_guess):
            origin = current_app.config.get("RESTAURANT_ADDRESS", "Bournemouth, UK")
            api_key = current_app.config.get("GOOGLE_MAPS_API_KEY", "")
            max_km = float(current_app.config.get("DELIVERY_MAX_KM", 5.0))

            if api_key:
                res = get_distance_and_eta_km(api_key=api_key, origin=origin, destination=postcode_guess)
                if res.ok and res.distance_km is not None:
                    delivery_info = {"km": float(res.distance_km), "eta": res.duration_text}
                    if float(res.distance_km) > float(max_km):
                        delivery_blocked = True

    # ✅ Hard stop ONLY when user submits order (POST)
    if request.method == "POST" and selected_type == "delivery" and delivery_blocked:
        flash("Sorry — this postcode is outside our delivery radius. Please choose Pickup instead.", "danger")
        return render_template(
            "customer/checkout.html",
            form=form,
            cart_rows=cart_rows,
            subtotal=subtotal,
            discount=Decimal("0.00"),
            discount_label=None,
            delivery_fee=Decimal("0.00"),
            total=subtotal,
            requires_payment=True,
            delivery_info=delivery_info,
            delivery_blocked=delivery_blocked,
            delivery_max_km=current_app.config.get("DELIVERY_MAX_KM", 5.0),
        )

    # -----------------------
    # ✅ PROMO LOGIC (NO STACKING)
    # Priority:
    # 1) first order 10% (min £15, cap £5) -> disables pickup 15%
    # 2) pickup 15%
    # -----------------------
    discount = Decimal("0.00")
    discount_label = None

    eligible_first_order = (
        is_first_order_eligible(current_user.id)
        and subtotal >= NEW_CUSTOMER_MIN_SPEND
        and subtotal > Decimal("0.00")
    )

    if eligible_first_order:
        discount = (subtotal * NEW_CUSTOMER_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if discount > NEW_CUSTOMER_CAP:
            discount = NEW_CUSTOMER_CAP
        discount_label = "New customer discount (10% off)"
    else:
        if selected_type == "pickup":
            discount = (subtotal * PICKUP_DISCOUNT_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            discount_label = "Pickup discount (15%)"

    # Delivery fee
    if selected_type == "delivery":
        delivery_fee = Decimal("0.00") if subtotal >= FREE_DELIVERY_THRESHOLD else DELIVERY_FEE
    else:
        delivery_fee = Decimal("0.00")

    total = (subtotal - discount + delivery_fee).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    requires_payment = (total > Decimal("0.00"))

    if not requires_payment:
        form.cardholder_name.validators = [Optional()]
        form.card_number.validators = [Optional()]
        form.expiry.validators = [Optional()]
        form.cvc.validators = [Optional()]

    if form.validate_on_submit():
        order_type = (form.order_type.data or "delivery").strip()

        # Recompute discount on POST using same rules
        discount = Decimal("0.00")
        discount_label = None

        eligible_first_order = (
            is_first_order_eligible(current_user.id)
            and subtotal >= NEW_CUSTOMER_MIN_SPEND
            and subtotal > Decimal("0.00")
        )

        if eligible_first_order:
            discount = (subtotal * NEW_CUSTOMER_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            if discount > NEW_CUSTOMER_CAP:
                discount = NEW_CUSTOMER_CAP
            discount_label = "New customer discount (10% off)"
        else:
            if order_type == "pickup":
                discount = (subtotal * PICKUP_DISCOUNT_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                discount_label = "Pickup discount (15%)"

        if order_type == "delivery":
            delivery_fee = Decimal("0.00") if subtotal >= FREE_DELIVERY_THRESHOLD else DELIVERY_FEE
        else:
            delivery_fee = Decimal("0.00")

        total = (subtotal - discount + delivery_fee).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        requires_payment = (total > Decimal("0.00"))

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
                    discount_label=discount_label,
                    delivery_fee=delivery_fee,
                    total=total,
                    requires_payment=requires_payment,
                    delivery_info=delivery_info,
                    delivery_blocked=delivery_blocked,
                    delivery_max_km=current_app.config.get("DELIVERY_MAX_KM", 5.0),
                )

            # Hard stop if outside radius (extra safety)
            if delivery_blocked:
                flash("Sorry — this postcode is outside our delivery radius.", "danger")
                return render_template(
                    "customer/checkout.html",
                    form=form,
                    cart_rows=cart_rows,
                    subtotal=subtotal,
                    discount=discount,
                    discount_label=discount_label,
                    delivery_fee=delivery_fee,
                    total=total,
                    requires_payment=requires_payment,
                    delivery_info=delivery_info,
                    delivery_blocked=delivery_blocked,
                    delivery_max_km=current_app.config.get("DELIVERY_MAX_KM", 5.0),
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
                    discount_label=discount_label,
                    delivery_fee=delivery_fee,
                    total=total,
                    requires_payment=requires_payment,
                    delivery_info=delivery_info,
                    delivery_blocked=delivery_blocked,
                    delivery_max_km=current_app.config.get("DELIVERY_MAX_KM", 5.0),
                )

        # If payment required, store demo last4
        if requires_payment:
            raw = (form.card_number.data or "").replace(" ", "")
            session["payment_last4"] = raw[-4:] if len(raw) >= 4 else None
        else:
            session["payment_last4"] = None

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

            if row.get("is_free"):
                unit_price = Decimal("0.00")
                line_total = Decimal("0.00")
            else:
                unit_price = Decimal(str(mi.price)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                line_total = (unit_price * qty).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            oi = OrderItem(
                order_id=order.id,
                menu_item_id=mi.id,
                quantity=qty,
                unit_price_at_time=unit_price,
                line_total=line_total,
            )
            db.session.add(oi)

        db.session.commit()

        earned = award_points_for_order(current_user.id, order.id, total)
        db.session.commit()

        # --- EMAIL CONFIRMATION (Cloud Run) ---
        from app.services.email_service import send_order_confirmation_via_cloudrun
        order_items = OrderItem.query.filter_by(order_id=order.id).all()

        try:
            for oi in order_items:
                _ = getattr(oi, "menu_item", None)
        except Exception:
            pass

        sent = send_order_confirmation_via_cloudrun(
            order=order,
            order_items=order_items,
            user_email=current_user.email,
)
        if not sent:
            current_app.logger.warning("Order email failed (Cloud Run). Check env vars / function logs.")
        # --- END EMAIL ---
            
        clear_cart()
        session["meal_deal_choices"] = {}
        session["free_item_ids"] = []
        session.modified = True

        log_event(
            "order_placed",
            {
                "order_id": order.id,
                "user_id": current_user.id,
                "order_type": order_type,
                "subtotal": str(subtotal),
                "discount": str(discount),
                "discount_label": discount_label,
                "delivery_fee": str(delivery_fee),
                "total": str(total),
                "items": [{"item_id": r["item"].id, "qty": r["qty"], "is_free": r.get("is_free", False)} for r in cart_rows],
                "loyalty_points_earned": earned,
            },
        )

        flash(f"Order placed successfully ✅ +{earned} reward points!", "success")
        return redirect(url_for("customer.order_confirmation", order_id=order.id))

    return render_template(
        "customer/checkout.html",
        form=form,
        cart_rows=cart_rows,
        subtotal=subtotal,
        discount=discount,
        discount_label=discount_label,
        delivery_fee=delivery_fee,
        total=total,
        requires_payment=requires_payment,
        delivery_info=delivery_info,
        delivery_blocked=delivery_blocked,
        delivery_max_km=current_app.config.get("DELIVERY_MAX_KM", 5.0),
    )


@customer_bp.get("/rewards")
@login_required
def rewards():
    acct = LoyaltyAccount.query.filter_by(user_id=current_user.id).first()
    if not acct:
        acct = LoyaltyAccount(
            user_id=current_user.id,
            points_balance=0,
            lifetime_earned=0,
            lifetime_redeemed=0,
        )
        db.session.add(acct)
        db.session.commit()

    txns = (
        LoyaltyTransaction.query
        .filter_by(user_id=current_user.id)
        .order_by(LoyaltyTransaction.ts.desc())
        .limit(20)
        .all()
    )

    # ✅ increased costs (harder to redeem)
    rewards_catalog = [
        {"id": "drink", "name": "Free Soft Drink", "cost": 150},
        {"id": "side", "name": "Free Side", "cost": 250},
        {"id": "dessert", "name": "Free Dessert", "cost": 400},
        {"id": "voucher5", "name": "£5 Off Voucher", "cost": 650},
    ]

    return render_template(
        "customer/rewards.html",
        points=acct.points_balance,
        txns=txns,
        rewards_catalog=rewards_catalog,
    )


@customer_bp.post("/rewards/redeem")
@login_required
def rewards_redeem():
    reward_id = (request.form.get("reward_id") or "").strip()

    rewards_map = {
        "drink": {"name": "Free Soft Drink", "cost": 150, "category": "Drinks"},
        "side": {"name": "Free Side", "cost": 250, "category": "Sides"},
        "dessert": {"name": "Free Dessert", "cost": 400, "category": "Desserts"},
        "voucher5": {"name": "£5 Off Voucher", "cost": 650, "category": None},
    }

    if reward_id not in rewards_map:
        flash("Invalid reward selection.", "danger")
        return redirect(url_for("customer.rewards"))

    acct = LoyaltyAccount.query.filter_by(user_id=current_user.id).first()
    if not acct:
        acct = LoyaltyAccount(
            user_id=current_user.id,
            points_balance=0,
            lifetime_earned=0,
            lifetime_redeemed=0,
        )
        db.session.add(acct)
        db.session.commit()

    reward = rewards_map[reward_id]
    cost = int(reward["cost"])

    if acct.points_balance < cost:
        flash("Not enough points to redeem this reward.", "warning")
        return redirect(url_for("customer.rewards"))

    # For now: voucher not implemented as cart item
    if reward_id == "voucher5":
        flash("Voucher redemption coming next (we’ll apply it at checkout).", "info")
        return redirect(url_for("customer.rewards"))

    # ✅ pick an actual item to give for free (cheapest in that category)
    free_item = (
        MenuItem.query
        .filter(MenuItem.is_available == True)  # noqa: E712
        .filter(MenuItem.category == reward["category"])
        .order_by(MenuItem.price.asc())
        .first()
    )
    if not free_item:
        flash("No available item found for this reward right now.", "warning")
        return redirect(url_for("customer.rewards"))

    # ✅ deduct points
    acct.points_balance -= cost
    acct.lifetime_redeemed += cost

    # ✅ add to cart normally
    add_to_cart(free_item.id, 1)

    # ✅ mark it as FREE in session
    free_ids = session.get("free_item_ids", []) or []
    if free_item.id not in free_ids:
        free_ids.append(free_item.id)
    session["free_item_ids"] = free_ids
    session.modified = True

    # ✅ record loyalty transaction using your schema (kind/points/note/ts)
    txn = LoyaltyTransaction(
        user_id=current_user.id,
        order_id=None,
        kind="redeem",
        points=cost,
        note=f"Redeemed: {reward['name']} → {free_item.name}",
    )
    db.session.add(txn)
    db.session.commit()

    flash(f"Redeemed {reward['name']} ✅ Added {free_item.name} to cart for FREE.", "success")
    return redirect(url_for("customer.cart_view"))


@customer_bp.get("/my-orders")
@login_required
def my_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template("customer/my_orders.html", orders=orders)

@customer_bp.get("/orders/<int:order_id>")
@login_required
def order_confirmation(order_id: int):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    last4 = session.pop("payment_last4", None)
    return render_template("customer/order_confirmation.html", order=order, last4=last4)
