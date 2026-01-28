from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.database.models import db, User

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
    template_folder="../templates"
)

# -------------------------------------------------
# ПРОВЕРКА ПРАВ АДМИНИСТРАТОРА
# -------------------------------------------------
def is_admin():
    return current_user.is_authenticated and current_user.role == "admin"


# -------------------------------------------------
# ГЛАВНАЯ СТРАНИЦА АДМИН-ПАНЕЛИ
# endpoint: admin.admin_index
# URL: /admin
# -------------------------------------------------
@admin_bp.route("/")
@login_required
def admin_index():
    if not is_admin():
        flash("Доступ запрещён", "error")
        return redirect(url_for("main.index"))

    return render_template("admin.html")


# -------------------------------------------------
# СПИСОК ПОЛЬЗОВАТЕЛЕЙ
# endpoint: admin.admin_users
# URL: /admin/users
# -------------------------------------------------
@admin_bp.route("/users")
@login_required
def admin_users():
    if not is_admin():
        flash("Доступ запрещён", "error")
        return redirect(url_for("main.index"))

    users = User.query.all()
    return render_template("admin_users.html", users=users)


# -------------------------------------------------
# СМЕНА РОЛИ ПОЛЬЗОВАТЕЛЯ
# endpoint: admin.change_user_role
# -------------------------------------------------
@admin_bp.route("/users/change-role/<int:user_id>", methods=["POST"])
@login_required
def change_user_role(user_id):
    if not is_admin():
        flash("Доступ запрещён", "error")
        return redirect(url_for("main.index"))

    user = User.query.get_or_404(user_id)
    new_role = request.form.get("role")

    if new_role not in ["admin", "user"]:
        flash("Некорректная роль", "error")
        return redirect(url_for("admin.admin_users"))

    user.role = new_role
    db.session.commit()

    flash("Роль пользователя обновлена", "success")
    return redirect(url_for("admin.admin_users"))


# -------------------------------------------------
# УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЯ
# endpoint: admin.delete_user
# -------------------------------------------------
@admin_bp.route("/users/delete/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    if not is_admin():
        flash("Доступ запрещён", "error")
        return redirect(url_for("main.index"))

    user = User.query.get_or_404(user_id)

    if user.username == "admin":
        flash("Нельзя удалить главного администратора", "error")
        return redirect(url_for("admin.admin_users"))

    db.session.delete(user)
    db.session.commit()

    flash("Пользователь удалён", "success")
    return redirect(url_for("admin.admin_users"))
