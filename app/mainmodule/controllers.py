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
from jinja2 import FileSystemLoader
from sqlalchemy.exc import SQLAlchemyError

module = Blueprint('mainmodule', __name__, url_prefix ='/')
module.jinja_loader = FileSystemLoader(['./app/templates', './app/mainmodule/templates'])

def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)

@module.route('/')
def main_page():
    return render_template('mainmodule/main_page.html', title='Главная страница')

from .forms import Login
@module.route('/login')
def login():
    form = Login()
    return render_template('mainmodule/login.html', form=form, title='Авторизация')

@module.route('/logout')
def logout():
    return redirect(url_for('main_page'))

from .forms import Register

@module.route('/register')
def register():
    form = Register()
    return render_template('mainmodule/register.html', form=form, title='Регистрация')

