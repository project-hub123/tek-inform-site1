import os
from flask import Flask
from flask_login import LoginManager

from config import DevelopmentConfig, ProductionConfig
from app.database.models import db, User

# ===== BLUEPRINTS САЙТА ООО «ТЭК ИНФОРМ» =====

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

    # ===== ВЫБОР КОНФИГУРАЦИИ =====
    if os.environ.get("RENDER"):
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # ===== ЗАЩИТА ОТ ОТСУТСТВИЯ SECRET_KEY =====
    if not app.config.get("SECRET_KEY"):
        app.config["SECRET_KEY"] = "dev-secret-key"

    # ===== ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ =====
    db.init_app(app)

    with app.app_context():
        db.create_all()

        # Создаём администратора ТОЛЬКО если его ещё нет
        admin_exists = User.query.filter_by(role="admin").first()
        if not admin_exists:
            create_admin()

    # ===== НАСТРОЙКА FLASK-LOGIN =====
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Пожалуйста, войдите в систему"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ===== РЕГИСТРАЦИЯ BLUEPRINTS =====
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
