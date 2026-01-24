from flask import Flask
from .config import DevConfig
from .extensions import db, login_manager, csrf

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"

    # Import models so SQLAlchemy registers them (we’ll add models next)
    from . import models  # noqa: F401

    # Register blueprints (we’ll create auth_routes next)
    from .routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    @app.get("/")
    def home():
        return "Restaurant Ordering App is running ✅"

    with app.app_context():
        db.create_all()

    return app
