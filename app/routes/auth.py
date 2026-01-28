from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user

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
    admin = User.query.filter_by(login="admin").first()
    if not admin:
        admin = User(login="admin", role="admin")
        admin.set_password("admin123")
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
        login_value = request.form.get("login")
        password = request.form.get("password")

        user = User.query.filter_by(login=login_value).first()

        if user and user.check_password(password):
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
        login_value = request.form.get("login")
        password = request.form.get("password")

        if User.query.filter_by(login=login_value).first():
            flash("Пользователь уже существует", "error")
            return redirect(url_for("auth.register"))

        user = User(login=login_value, role="user")
        user.set_password(password)

        db.session.add(user)
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
    return current_user.is_authenticated and current_user.role == "admin"
