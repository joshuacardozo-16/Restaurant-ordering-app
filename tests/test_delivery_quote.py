from types import SimpleNamespace


def test_delivery_quote_invalid_postcode(login_user):
    resp = login_user.get("/delivery-quote?postcode=INVALID")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["ok"] is False
    assert data["error"] == "invalid_postcode"


def test_delivery_quote_valid_postcode_mocks_maps(login_user, monkeypatch):
    # Patch the function used in your route:
    # from ..services.maps_distance import get_distance_and_eta_km
    from app.routes import customer_routes

    def fake_get_distance_and_eta_km(api_key, origin, destination):
        return SimpleNamespace(ok=True, distance_km=3.2, duration_text="12 mins")

    monkeypatch.setattr(customer_routes, "get_distance_and_eta_km", fake_get_distance_and_eta_km)

    resp = login_user.get("/delivery-quote?postcode=BH1 1AA")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["ok"] is True
    assert data["distance_km"] == 3.2
    assert data["blocked"] is False
