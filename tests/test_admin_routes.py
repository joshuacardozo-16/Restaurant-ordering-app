def test_admin_dashboard_requires_login(client):
    resp = client.get("/admin/", follow_redirects=False)
    assert resp.status_code in (302, 401)


def test_admin_dashboard_forbidden_for_customer(login_user):
    resp = login_user.get("/admin/", follow_redirects=False)
    assert resp.status_code == 403


def test_admin_dashboard_allowed_for_admin(login_admin):
    resp = login_admin.get("/admin/", follow_redirects=False)
    assert resp.status_code in (200, 302)
