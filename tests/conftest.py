import pytest

from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.menu_item import MenuItem


@pytest.fixture
def app(monkeypatch):
    # ✅ MUST set DATABASE_URL BEFORE create_app()
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")

    # Minimal env so config loads cleanly
    monkeypatch.setenv("SECRET_KEY", "test-secret")
    monkeypatch.setenv("GOOGLE_MAPS_API_KEY", "test-maps-key")
    monkeypatch.setenv("RESTAURANT_ADDRESS", "Bournemouth, UK")
    monkeypatch.setenv("DELIVERY_MAX_KM", "5")
    monkeypatch.setenv("ORDER_EMAIL_FUNCTION_URL", "https://example.com/fake-email-fn")
    monkeypatch.setenv("FUNCTION_SHARED_SECRET", "test-shared-secret")

    app = create_app()

    # ✅ only test flags here (DO NOT override SQLALCHEMY_DATABASE_URI here)
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        LOGIN_DISABLED=False,
    )

    with app.app_context():
        # ✅ HARD SAFETY CHECK: refuse to run if DB is not in-memory
        db_url = str(db.engine.url).replace("\\", "/").lower()
        assert ":memory:" in db_url, f"Refusing to run tests on DB: {db.engine.url}"
        assert "instance/local.db" not in db_url, f"Refusing to run tests on prod DB: {db.engine.url}"

        # ✅ IMPORTANT: no drop_all() (no chance of wiping real DB)
        db.create_all()

        # Seed users
        admin = User(
            email="admin@test.com",
            full_name="Admin User",
            phone=None,
            role="admin",
            password_hash=generate_password_hash("AdminPass123"),
        )
        user = User(
            email="user@test.com",
            full_name="Normal User",
            phone=None,
            role="customer",
            password_hash=generate_password_hash("UserPass123"),
        )
        db.session.add_all([admin, user])

        # Seed menu
        mi1 = MenuItem(
            name="Butter Chicken",
            description="Creamy curry",
            price=14.50,
            category="Mains",
            image_url=None,
            is_available=True,
        )
        mi2 = MenuItem(
            name="Coke",
            description="Soft drink",
            price=2.50,
            category="Drinks",
            image_url=None,
            is_available=True,
        )
        db.session.add_all([mi1, mi2])
        db.session.commit()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def _login(client, email, password):
    return client.post(
        "/auth/login",
        data={"email": email, "password": password},
        follow_redirects=False,
    )


@pytest.fixture
def login_user(client):
    resp = _login(client, "user@test.com", "UserPass123")
    assert resp.status_code in (302, 200)
    return client


@pytest.fixture
def login_admin(client):
    resp = _login(client, "admin@test.com", "AdminPass123")
    assert resp.status_code in (302, 200)
    return client
