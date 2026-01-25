from flask import Flask, render_template
from .config import DevConfig
from .extensions import db, login_manager, csrf

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)

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


    @app.get("/")
    def home():
        return render_template("home.html")

    with app.app_context():
        db.create_all()

    return app
