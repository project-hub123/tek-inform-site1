from flask import Flask
from flask_login import LoginManager

from config import DevelopmentConfig
from app.database.models import db

# ===== BLUEPRINTS САЙТА ООО «ТЭК ИНФОРМ» =====

from app.routes.main import main_bp              # Главная, О компании, Контакты, Карта сайта
from app.routes.services import services_bp      # Услуги
from app.routes.articles import articles_bp      # Статьи
from app.routes.news import news_bp               # Новости
from app.routes.users import users_bp             # Личный кабинет
from app.routes.admin import admin_bp             # Административная панель
from app.routes.errors import errors_bp            # Ошибки 404, 403

from app.components.auth import auth_bp, create_admin
from app.components.search_engine import search_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    # ===== ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ =====
    db.init_app(app)

    with app.app_context():
        db.create_all()
        # Создание администратора при первом запуске
        create_admin()

    # ===== НАСТРОЙКА FLASK-LOGIN =====
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Пожалуйста, войдите в систему"
    login_manager.init_app(app)

    from app.database.models import User

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
