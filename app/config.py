import os

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-change-me")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # DB (fallback local sqlite)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///local.db")

    # Google Maps (NO hardcoded key)
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")
    RESTAURANT_ADDRESS = os.getenv("RESTAURANT_ADDRESS", "Bournemouth, UK")
    DELIVERY_MAX_KM = float(os.getenv("DELIVERY_MAX_KM", "5"))

    # Email function (optional; used by your email service)
    ORDER_EMAIL_FUNCTION_URL = os.getenv("ORDER_EMAIL_FUNCTION_URL", "")
    FUNCTION_SHARED_SECRET = os.getenv("FUNCTION_SHARED_SECRET", "")

class DevConfig(BaseConfig):
    DEBUG = True

class ProdConfig(BaseConfig):
    DEBUG = False
