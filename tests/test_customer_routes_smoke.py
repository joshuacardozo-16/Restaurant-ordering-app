from decimal import Decimal

def test_menu_page_loads(login_user, monkeypatch):
    # Avoid Firestore + background threads in unit tests
    from app.routes import customer_routes

    monkeypatch.setattr(customer_routes, "get_popular_ids_cached", lambda: set(), raising=True)
    monkeypatch.setattr(customer_routes, "log_event", lambda *a, **k: None, raising=True)

    resp = login_user.get("/menu")
    assert resp.status_code == 200


def test_cart_page_loads(login_user, monkeypatch, app):
    from app.routes import customer_routes
    from app.models.menu_item import MenuItem

    monkeypatch.setattr(customer_routes, "log_event", lambda *a, **k: None, raising=True)

    # Put a real item into cart
    with app.app_context():
        item = MenuItem.query.first()
        assert item is not None

    with login_user.session_transaction() as sess:
        sess["cart"] = {str(item.id): 2}
        sess["free_item_ids"] = []
        sess["meal_deal_choices"] = {}

    resp = login_user.get("/cart")
    assert resp.status_code == 200


def test_checkout_get_loads_when_cart_present(login_user, monkeypatch, app):
    from app.routes import customer_routes
    from app.models.menu_item import MenuItem

    # Prevent Firestore thread + event write noise
    monkeypatch.setattr(customer_routes, "log_event", lambda *a, **k: None, raising=True)

    with app.app_context():
        item = MenuItem.query.first()
        assert item is not None

    with login_user.session_transaction() as sess:
        sess["cart"] = {str(item.id): 1}
        sess["free_item_ids"] = []
        sess["meal_deal_choices"] = {}

    # Pickup avoids Google Maps distance calls
    resp = login_user.get("/checkout?order_type=pickup")
    assert resp.status_code == 200


def test_my_orders_page_loads(login_user):
    resp = login_user.get("/my-orders")
    assert resp.status_code == 200
