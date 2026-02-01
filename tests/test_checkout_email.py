def test_checkout_triggers_email(login_user, app, monkeypatch):
    from app.models.menu_item import MenuItem
    import app.services.email_service as email_service

    # -----------------------------
    # Mock Cloud Run email function (PATCH THE RIGHT PLACE)
    # -----------------------------
    calls = {"sent": 0}

    def fake_send(order, order_items, user_email):
        calls["sent"] += 1
        return True

    monkeypatch.setattr(email_service, "send_order_confirmation_via_cloudrun", fake_send)

    # -----------------------------
    # Get a real seeded menu item (no hardcoded IDs)
    # -----------------------------
    with app.app_context():
        item = MenuItem.query.first()
        assert item is not None, "No menu items seeded in test DB"
        item_id = item.id

    # -----------------------------
    # Put item into cart session
    # -----------------------------
    with login_user.session_transaction() as sess:
        sess["cart"] = {str(item_id): 1}
        sess["free_item_ids"] = []

    # -----------------------------
    # Submit checkout (pickup simplest)
    # -----------------------------
    resp = login_user.post(
        "/checkout",
        data={
            "order_type": "pickup",
            "pickup_time_requested": "18:30",

            # payment fields
            "cardholder_name": "Test User",
            "card_number": "1234 5678 9012 3456",
            "expiry": "12/30",
            "cvc": "123",
        },
        follow_redirects=False,
    )

    # -----------------------------
    # Assertions
    # -----------------------------
    assert resp.status_code in (302, 200)
    assert calls["sent"] == 1
