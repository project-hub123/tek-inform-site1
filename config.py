import os

class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = "super-secret-key"

    # Папка проекта (где лежит config.py)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Путь к базе в app/database/db.sqlite3
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        BASE_DIR, "app", "database", "db.sqlite3"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
