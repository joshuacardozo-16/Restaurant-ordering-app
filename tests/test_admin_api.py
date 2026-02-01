def test_admin_menu_requires_login(client):
    resp = client.get("/api/admin/menu")
    assert resp.status_code in (302, 401)


def test_admin_menu_forbidden_for_customer(login_user):
    resp = login_user.get("/api/admin/menu")
    assert resp.status_code == 403


def test_admin_menu_list_allowed_for_admin(login_admin):
    resp = login_admin.get("/api/admin/menu")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "items" in data
    assert data["count"] >= 1


def test_admin_menu_create_update_delete(login_admin):
    # CREATE
    create = login_admin.post(
        "/api/admin/menu",
        json={"name": "Test Item", "category": "Sides", "price": 3.99},
    )
    assert create.status_code == 201
    created = create.get_json()["created"]
    item_id = created["id"]

    # UPDATE
    upd = login_admin.put(
        f"/api/admin/menu/{item_id}",
        json={"name": "Updated Item", "price": 4.50, "is_available": False},
    )
    assert upd.status_code == 200
    updated = upd.get_json()["updated"]
    assert updated["name"] == "Updated Item"
    assert updated["price"] == "4.50"
    assert updated["is_available"] is False

    # DELETE
    delete = login_admin.delete(f"/api/admin/menu/{item_id}")
    assert delete.status_code == 200
    assert delete.get_json()["deleted_id"] == item_id
