from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

# -----------------------------------
# МОДЕЛЬ ПОЛЬЗОВАТЕЛЯ
# -----------------------------------
class User(db.Model):
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
# МОДЕЛИ ДЛЯ СТАТЕЙ, НОВОСТЕЙ И СООБЩЕНИЙ
# -----------------------------------
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(50), default=datetime.now().strftime("%Y-%m-%d"))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default="Гость")
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(50), default=datetime.now().strftime("%Y-%m-%d %H:%M"))
