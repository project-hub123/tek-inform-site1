from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.database.models import db, User

auth_bp = Blueprint(
    "auth",
    __name__,
    template_folder="../templates"
)


# -------------------------------------------------
# СОЗДАНИЕ АДМИНИСТРАТОРА ПРИ ПЕРВОМ ЗАПУСКЕ
# -------------------------------------------------
def create_admin():
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(
            username="admin",
            password_hash=generate_password_hash("admin123"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()


# -------------------------------------------------
# ВХОД В СИСТЕМУ
# -------------------------------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("main.index"))

        flash("Неверный логин или пароль", "error")

    return render_template("login.html")


# -------------------------------------------------
# РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ
# -------------------------------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if User.query.filter_by(username=username).first():
            flash("Пользователь уже существует", "error")
            return redirect(url_for("auth.register"))

        new_user = User(
            username=username,
            password_hash=generate_password_hash(password),
            role="user"
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Регистрация прошла успешно", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


# -------------------------------------------------
# ВЫХОД ИЗ СИСТЕМЫ
# -------------------------------------------------
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


# -------------------------------------------------
# ПРОВЕРКА ДОСТУПА АДМИНИСТРАТОРА
# -------------------------------------------------
def admin_required():
    if not current_user.is_authenticated or current_user.role != "admin":
        return False
    return True
