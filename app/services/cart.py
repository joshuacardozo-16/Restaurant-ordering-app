from flask import session

CART_KEY = "cart"  # dict: {menu_item_id: quantity}

def get_cart() -> dict:
    return session.get(CART_KEY, {})

def add_to_cart(item_id: int, qty: int = 1) -> None:
    cart = session.get(CART_KEY, {})
    key = str(item_id)
    cart[key] = int(cart.get(key, 0)) + int(qty)
    session[CART_KEY] = cart
    session.modified = True

def remove_from_cart(item_id: int) -> None:
    cart = session.get(CART_KEY, {})
    cart.pop(str(item_id), None)
    session[CART_KEY] = cart
    session.modified = True

def clear_cart() -> None:
    session.pop(CART_KEY, None)
    session.modified = True

def set_qty(item_id: int, qty: int) -> None:
    cart = session.get(CART_KEY, {})
    key = str(item_id)
    qty = int(qty)

    if qty <= 0:
        cart.pop(key, None)
    else:
        cart[key] = qty

    session[CART_KEY] = cart
    session.modified = True


