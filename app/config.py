import os


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-change-me")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ✅ CRITICAL:
    # Use DATABASE_URL if provided (Cloud / Tests)
    # Otherwise fallback to local SQLite safely
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///local.db"
    )

    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")
    RESTAURANT_ADDRESS = os.getenv("RESTAURANT_ADDRESS", "Bournemouth, UK")
    DELIVERY_MAX_KM = float(os.getenv("DELIVERY_MAX_KM", "5"))

    ORDER_EMAIL_FUNCTION_URL = os.getenv("ORDER_EMAIL_FUNCTION_URL", "")
    FUNCTION_SHARED_SECRET = os.getenv("FUNCTION_SHARED_SECRET", "")


class DevConfig(BaseConfig):
    DEBUG = True


class ProdConfig(BaseConfig):
    DEBUG = False
