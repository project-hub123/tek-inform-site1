import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "tek-inform-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # КРИТИЧЕСКИ ВАЖНО
    # Flask-WTF установлен → CSRF включён по умолчанию → POST = 500
    WTF_CSRF_ENABLED = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "site.db")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "site.db")
    )
