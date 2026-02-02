import os

def test_send_email_success(monkeypatch):
    from app.services import email_service

    # Provide required env vars
    monkeypatch.setenv("SENDGRID_API_KEY", "test-key")
    monkeypatch.setenv("SENDGRID_FROM_EMAIL", "from@test.com")
    monkeypatch.setenv("SENDGRID_FROM_NAME", "Test Sender")

    class FakeResp:
        status_code = 202

    class FakeClient:
        def __init__(self, *a, **k):
            pass
        def send(self, message):
            return FakeResp()

    monkeypatch.setattr(email_service, "SendGridAPIClient", FakeClient, raising=True)

    ok = email_service.send_email("to@test.com", "Subject", "<p>Hello</p>")
    assert ok is True


def test_send_order_confirmation_via_cloudrun_success(monkeypatch):
    from app.services import email_service

    monkeypatch.setenv("ORDER_EMAIL_FUNCTION_URL", "https://example.com/fn")
    monkeypatch.setenv("FUNCTION_SHARED_SECRET", "secret")

    class FakeResponse:
        ok = True
        headers = {"content-type": "application/json"}
        def json(self):
            return {"ok": True}

    def fake_post(url, json=None, headers=None, timeout=None):
        assert "X-FUNCTION-SECRET" in (headers or {})
        return FakeResponse()

    monkeypatch.setattr(email_service.requests, "post", fake_post, raising=True)

    # minimal dummy objects
    order = type("Order", (), {"id": 1, "total_price": "9.99", "order_type": "pickup"})()
    oi = type("OI", (), {"quantity": 1, "unit_price_at_time": "9.99", "menu_item_id": 1,
                         "menu_item": type("MI", (), {"name": "Test Item"})()})()

    ok = email_service.send_order_confirmation_via_cloudrun(order, [oi], "user@test.com")
    assert ok is True
