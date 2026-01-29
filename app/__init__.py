import os
from flask import Flask
from flask_login import LoginManager

from config import DevelopmentConfig, ProductionConfig
from app.database.models import db, User

from app.routes.main import main_bp
from app.routes.services import services_bp
from app.routes.articles import articles_bp
from app.routes.news import news_bp
from app.routes.users import users_bp
from app.routes.admin import admin_bp
from app.routes.errors import errors_bp

from app.components.auth import auth_bp, create_admin
from app.components.search_engine import search_bp


def create_app():
    app = Flask(__name__)

    # ===== КОНФИГУРАЦИЯ =====
    if os.environ.get("RENDER"):
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # ===== БАЗА ДАННЫХ (ТОЛЬКО ИЗ ENV) =====
    database_url = os.environ["DATABASE_URL"]

    if database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://", "postgresql+psycopg2://", 1
        )
    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace(
            "postgresql://", "postgresql+psycopg2://", 1
        )

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ===== SECRET KEY ТОЛЬКО ИЗ ENV =====
    app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

    # ===== ИНИЦИАЛИЗАЦИЯ БД =====
    db.init_app(app)

    with app.app_context():
        db.create_all()

        admin_exists = User.query.filter_by(role="admin").first()
        if not admin_exists:
            create_admin()

    # ===== FLASK-LOGIN =====
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Пожалуйста, войдите в систему"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # ===== BLUEPRINTS =====
    app.register_blueprint(main_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(articles_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(errors_bp)

    return app
