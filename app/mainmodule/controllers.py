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
    get_flashed_messages,
)
from jinja2 import FileSystemLoader
from flask_login import login_required, login_user, current_user, logout_user
from .. import login_manager

module = Blueprint('mainmodule', __name__, url_prefix ='/')
module.jinja_loader = FileSystemLoader(['./app/templates', './app/mainmodule/templates'])

@login_manager.unauthorized_handler
def handle_needs_login():
    flash("Вы должны сначала авторизироваться на сайте.", 'warning')
    return redirect(url_for('.login', next=request.endpoint))

def redirect_dest(fallback=None):
    with current_app.app_context():
        if not fallback:
            fallback=url_for('.main_page')
        dest = request.args.get('next')
        try:
            dest_url = url_for(dest)
            return redirect(dest_url)
        except:
            return redirect(fallback)

def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)

@module.route('/')
def main_page():
    return render_template('mainmodule/main_page.html', title='Главная страница')

from ..database import get_user_by_id

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)['result']

from .forms import Login
from ..database import check_user_entered_data

@module.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect_dest()
    form = Login()
    if request.method == 'POST':
        if form.validate_on_submit():
            api_res = check_user_entered_data(form.email.data, form.password.data)
            match api_res['status']:
                case 200:
                    user = load_user(api_res['result'])
                    if user:
                        login_user(user, remember=form.remember_me.data)
                        flash('Вы успешно вошли в систему!', 'success')
                        return redirect_dest()
                    return render_template('mainmodule/login.html', form=form, title='Авторизация', messages=[('error', 'Ошибка на сайте. Повторите попытку позже.')])
                case 401:
                    return render_template('mainmodule/login.html', form=form, title='Авторизация', messages=[('error', 'Ошибка входа. Проверьте введенные данные.')])
                case 500:
                    return render_template('mainmodule/login.html', form=form, title='Авторизация', messages=[('error', 'Ошибка на сайте. Повторите попытку позже.')])
        else:
            return render_template('mainmodule/login.html', form=form, user=current_user, title='Авторизация', messages=[('error', 'Ошибка входа. Проверьте введенные данные.')])
    return render_template('mainmodule/login.html', form=form, title='Авторизация')

@module.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы успешно вышли из системы!", 'success')
    return redirect(url_for('.main_page'))

from .forms import Register
from ..database import register_new_user

@module.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect_dest()
    form = Register()
    if request.method == 'POST':
        if form.validate_on_submit():
            api_res = register_new_user(form.first_name.data, form.last_name.data, form.email.data, form.password1.data)
            match api_res['status']:
                case 200:
                    user = load_user(api_res['result'])
                    if user:
                        login_user(user, remember=form.remember_me.data)
                        flash('Вы успешно зарегистрировались!', 'success')
                        return redirect_dest()
                    render_template('mainmodule/register.html', form=form, title='Регистрация',
                           messages=[('error', 'Ошибка на сайте. Повторите попытку позже.')])
                case 401:
                    render_template('mainmodule/register.html', form=form, title='Регистрация',
                           messages=[('error', 'Ошибка регистрации. Проверьте введенные данные.')])
                case 500:
                    render_template('mainmodule/register.html', form=form, title='Регистрация',
                           messages=[('error', 'Ошибка на сайте. Повторите попытку позже.')])
        else:
            return render_template('mainmodule/register.html', form=form, title='Регистрация')
    return render_template('mainmodule/register.html', form=form, title='Регистрация')

