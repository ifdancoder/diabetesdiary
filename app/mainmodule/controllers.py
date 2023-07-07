# ВНИМАНИЕ: код для примера! Не нужно его бездумно копировать!
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    abort,
    redirect,
    url_for,
    current_app,
)
from sqlalchemy.exc import SQLAlchemyError

module = Blueprint('mainmodule', __name__, url_prefix ='/')


def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)

@module.route('/')
def main_page():
    return render_template('base.html')

@module.route('/login')
def login():
    return render_template('login.html')

@module.route('/logout')
def logout():
    return redirect(url_for('main_page'))

@module.route('/register')
def register():
    return render_template('register.html')

