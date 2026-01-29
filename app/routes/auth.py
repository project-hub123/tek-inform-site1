from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

from app.database.models import db, User

auth_bp = Blueprint(
    "auth",
    __name__,
    template_folder="../templates"
)

# -------------------------------------------------
# СОЗДАНИЕ АДМИНИСТРАТОРА
# -------------------------------------------------
def create_admin():
    admin = User.query.filter_by(login="admin").first()
    if admin:
        return

    admin = User(
        login="admin",
        role="admin"
    )
    admin.set_password("admin123")

    db.session.add(admin)
    db.session.commit()

# -------------------------------------------------
# ВХОД
# -------------------------------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        login_value = request.form.get("login", "").strip()
        password = request.form.get("password", "").strip()

        if not login_value or not password:
            flash("Введите логин и пароль", "error")
            return redirect(url_for("auth.login"))

        user = User.query.filter_by(login=login_value).first()

        if not user or not user.password_hash:
            flash("Неверный логин или пароль", "error")
            return redirect(url_for("auth.login"))

        if check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("main.index"))

        flash("Неверный логин или пароль", "error")
        return redirect(url_for("auth.login"))

    return render_template("login.html")

# -------------------------------------------------
# РЕГИСТРАЦИЯ
# -------------------------------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        login_value = request.form.get("login", "").strip()
        password = request.form.get("password", "").strip()

        if not login_value or not password:
            flash("Логин и пароль обязательны", "error")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(login=login_value).first():
            flash("Пользователь уже существует", "error")
            return redirect(url_for("auth.register"))

        try:
            user = User(
                login=login_value,
                role="user"
            )
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            flash("Регистрация прошла успешно", "success")
            return redirect(url_for("auth.login"))

        except Exception:
            db.session.rollback()
            flash("Ошибка при регистрации", "error")
            return redirect(url_for("auth.register"))

    return render_template("register.html")

# -------------------------------------------------
# ВЫХОД
# -------------------------------------------------
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
