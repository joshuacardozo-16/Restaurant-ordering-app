from flask import Blueprint

api_bp = Blueprint("api", __name__, url_prefix="/api")

# import routes so they register with blueprint
from . import menu_api  # noqa: F401
from . import order_api  # noqa: F401
from . import admin_api  # noqa: F401 (we’ll fill later)
