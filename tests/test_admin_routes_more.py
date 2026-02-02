def test_admin_dashboard_as_admin(login_admin):
    resp = login_admin.get("/admin/")
    assert resp.status_code == 200


def test_admin_dashboard_forbidden_for_customer(login_user):
    resp = login_user.get("/admin/")
    # depending on your abort handling, could be 403
    assert resp.status_code in (403, 302)


def test_admin_orders_page_as_admin(login_admin):
    resp = login_admin.get("/admin/orders")
    assert resp.status_code == 200


def test_admin_menu_page_as_admin(login_admin):
    resp = login_admin.get("/admin/menu")
    assert resp.status_code == 200
