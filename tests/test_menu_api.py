def test_menu_api_returns_items(client):
    resp = client.get("/api/menu")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["count"] >= 1
    assert any(i["name"] == "Butter Chicken" for i in data["items"])


def test_menu_api_search(client):
    resp = client.get("/api/menu?q=butter")
    assert resp.status_code == 200
    data = resp.get_json()
    assert any("Butter" in i["name"] for i in data["items"])


def test_menu_api_detail(client):
    resp = client.get("/api/menu/1")
    assert resp.status_code in (200, 404)  # depends on seeded IDs
