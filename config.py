import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "tek-inform-2026")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-WTF установлен → отключаем CSRF
    WTF_CSRF_ENABLED = False


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    pass
