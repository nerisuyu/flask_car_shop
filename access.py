from flask import session, current_app, request, render_template
from functools import wraps


def group_validation():
    group_name = session.get('group_name', '')
    if group_name:
        return True
    else:
        return False


def group_validation_decorator(f):
    @wraps(f)  # похволяет сохранять метадату самой функции а не wrapper'a
    def wrapper(*args, **kwargs):
        if group_validation():
            return f(*args, **kwargs)  # запуск
        return 'Permission denied'

    return wrapper  # вызов


def group_permission_validation():
    access_config = current_app.config['access_config']
    group_name = session.get('group_name', 'unauthorized')
    # request.endpoint = /auth/login => 'auth.login_page' -// имя функции обработчика// = ['auth', 'login_page']
    # request.endpoint = /get-name => 'select-user'
    # if group_name == 'admin':
    target_app = "" if len(request.endpoint.split('.')) == 1 else request.endpoint.split('.')[1]
    # else:
    # target_app = "" if len(request.endpoint.split('.')) == 1 else request.endpoint.split('.')[1]
    if group_name in access_config and target_app in access_config[group_name]:
        return True


def group_permission_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if group_permission_validation():
            return f(*args, **kwargs)
        return render_template("access_error.html")

    return wrapper
