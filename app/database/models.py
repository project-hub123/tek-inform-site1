from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

# -----------------------------------
# МОДЕЛЬ ПОЛЬЗОВАТЕЛЯ
# -----------------------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")  # user / admin

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.login}>"

# -----------------------------------
# МОДЕЛЬ СТАТЕЙ
# -----------------------------------
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Article {self.title}>"

# -----------------------------------
# МОДЕЛЬ НОВОСТЕЙ
# -----------------------------------
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(
        db.String(50),
        default=lambda: datetime.now().strftime("%Y-%m-%d")
    )

    def __repr__(self):
        return f"<News {self.title}>"

# -----------------------------------
# МОДЕЛЬ СООБЩЕНИЙ
# -----------------------------------
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default="Гость")
    text = db.Column(db.Text, nullable=False)
    date = db.Column(
        db.String(50),
        default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M")
    )

    def __repr__(self):
        return f"<Message {self.id}>"
