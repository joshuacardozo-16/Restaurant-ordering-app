from decimal import Decimal
from app.extensions import db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.menu_item import MenuItem
from app.models.user import User


def test_orders_api_requires_login(client):
    resp = client.get("/api/orders")
    assert resp.status_code in (302, 401)


def test_orders_api_list_and_detail(login_user, app):
    with app.app_context():
        user = User.query.filter_by(email="user@test.com").first()
        item = MenuItem.query.first()

        o = Order(
            user_id=user.id,
            order_type="pickup",
            status="pending",
            total_price=Decimal("10.00"),
        )
        db.session.add(o)
        db.session.flush()

        oi = OrderItem(
            order_id=o.id,
            menu_item_id=item.id,
            quantity=1,
            unit_price_at_time=Decimal("10.00"),
            line_total=Decimal("10.00"),
        )
        db.session.add(oi)
        db.session.commit()
        order_id = o.id

    resp = login_user.get("/api/orders")
    assert resp.status_code == 200
    data = resp.get_json()
    assert any(o["id"] == order_id for o in data["orders"])

    detail = login_user.get(f"/api/orders/{order_id}")
    assert detail.status_code == 200
    d = detail.get_json()
    assert d["order"]["id"] == order_id
    assert len(d["items"]) >= 1
