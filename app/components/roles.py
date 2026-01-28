from flask import session, redirect, url_for


def current_user():
    """
    Возвращает логин текущего пользователя или None
    """
    return session.get('user')


def current_role():
    """
    Возвращает роль текущего пользователя (admin/user) или None
    """
    return session.get('role')


def login_required(func):
    """
    Декоратор: доступ только авторизованным пользователям
    """
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


def admin_required(func):
    """
    Декоратор: доступ только администратору
    """
    def wrapper(*args, **kwargs):
        if session.get('role') != 'admin':
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
