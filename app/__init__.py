from flask import Flask, render_template
from .config import DevConfig
from .extensions import db, login_manager, csrf
from .models.loyalty import LoyaltyAccount
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)

    # ✅ Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # ✅ Use DATABASE_URL if provided (tests will set this),
    # otherwise use your real local DB in instance/local.db
    db_uri = os.getenv("DATABASE_URL")
    if db_uri:
        app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    else:
        db_path = os.path.join(app.instance_path, "local.db")
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path.replace("\\", "/")

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"

    # Import models so SQLAlchemy registers them
    from . import models  # noqa: F401

    # Register blueprints
    from .routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    from .routes.admin_routes import admin_bp
    app.register_blueprint(admin_bp)

    from .routes.customer_routes import customer_bp
    app.register_blueprint(customer_bp)

    # ✅ (If you have API blueprint, keep it)
    from .api import api_bp
    csrf.exempt(api_bp)
    app.register_blueprint(api_bp)

    # ✅ Inject loyalty points into ALL templates
    @app.context_processor
    def inject_loyalty_points():
        points = 0
        try:
            from flask_login import current_user
            if current_user.is_authenticated:
                acct = LoyaltyAccount.query.filter_by(user_id=current_user.id).first()
                points = acct.points_balance if acct else 0
        except Exception:
            points = 0
        return {"loyalty_points": points}

    @app.get("/")
    def home():
        return render_template("home.html")

    # ✅ Only create tables in normal app run, not tests
    if not app.config.get("TESTING"):
        with app.app_context():
            db.create_all()

    return app
