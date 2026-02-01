from app.models.user import User
from app.extensions import db


def test_register_creates_user(client, app):
    resp = client.post(
        "/auth/register",
        data={
            "full_name": "New User",
            "phone": "07000000000",
            "email": "new@test.com",
            "password": "StrongPass123",
            "confirm_password": "StrongPass123",
        },
        follow_redirects=False,
    )
    assert resp.status_code in (302, 200)

    with app.app_context():
        u = User.query.filter_by(email="new@test.com").first()
        assert u is not None
        assert u.check_password("StrongPass123")


def test_register_rejects_weak_password(client):
    # Your validator requires uppercase, lowercase, number, min 8
    resp = client.post(
        "/auth/register",
        data={
            "full_name": "Weak User",
            "phone": "",
            "email": "weak@test.com",
            "password": "password",   # fails: no uppercase + no number
            "confirm_password": "password",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"uppercase" in resp.data or b"number" in resp.data or b"Password must" in resp.data


def test_login_logout_flow(client):
    r = client.post("/auth/login", data={"email": "user@test.com", "password": "UserPass123"})
    assert r.status_code in (302, 200)

    out = client.get("/auth/logout", follow_redirects=False)
    assert out.status_code in (302, 200)
