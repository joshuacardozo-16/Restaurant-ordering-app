from flask import Flask, render_template
from .config import DevConfig, ProdConfig
from .extensions import db, login_manager, csrf
from .models.loyalty import LoyaltyAccount
import os


def create_app():
    app = Flask(__name__)

    # Use production config on App Engine, dev otherwise
    if os.getenv("GAE_ENV", "").startswith("standard"):
        app.config.from_object(ProdConfig)
    else:
        app.config.from_object(DevConfig)

    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # If DATABASE_URL exists, use it. Otherwise use instance/local.db
    db_uri = os.getenv("DATABASE_URL")
    if db_uri:
        app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    else:
        db_path = os.path.join(app.instance_path, "local.db")
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path.replace("\\", "/")

    # Init extensions (ALWAYS)
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

    # API blueprint
    from .api import api_bp
    csrf.exempt(api_bp)
    app.register_blueprint(api_bp)

    # Inject loyalty points into ALL templates
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

    # Create tables if not testing (does not wipe)
    if not app.config.get("TESTING"):
        with app.app_context():
            db.create_all()

    return app
