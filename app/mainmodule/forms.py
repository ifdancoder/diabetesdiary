from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, Optional
from datetime import datetime

class Login(FlaskForm):
    email = StringField('Имя пользователя или email', validators=[DataRequired(message='Это поле обязательно для заполнения'), Email(message='Введите корректный email')])
    password = PasswordField('Пароль', validators=[DataRequired(message='Это поле обязательно для заполнения')])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Вход')

from .custom_validators import existing_email
class Register(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired(message='Это поле обязательно для заполнения'), Length(min=2, max=50, message='Введите корректное имя (от 2 до 50 символов)')])
    last_name = StringField('Фамилия', validators=[DataRequired(message='Это поле обязательно для заполнения'), Length(min=2, max=50, message='Введите корректную фамилию (от 2 до 50 символов)')])
    email = StringField('Email', validators=[DataRequired(message='Это поле обязательно для заполнения'), Email(message='Введите корректный email'), existing_email()])
    password1 = PasswordField('Пароль', validators=[DataRequired(message='Это поле обязательно для заполнения'), Length(min=8, max=50, message='Придумайте пароль сложнее')])
    password2 = PasswordField('Повтор пароля', validators=[DataRequired(message='Это поле обязательно для заполнения'), EqualTo('password1', message='Пароли не совпадают')])
    remember_me = BooleanField('Запомнить меня после входа')
    submit = SubmitField('Регистрация и вход')

class BasalInsulin(FlaskForm):
    def __init__(self, field_count=24, *args, **kwargs):
        super(BasalInsulin, self).__init__(*args, **kwargs)
        for i in range(field_count):
            field_name = f'insulin_{i}'
            field_label = f'Базальный инсулин ({i:02d}:{(i + 1):02d}):'
            setattr(self, field_name, DecimalField(field_label), validators=[Optional(), NumberRange(min=0.01, max=5, message='Введите число от 0.01 до 5')])
        self.submit = SubmitField('Запись')

class DiaryRecord(FlaskForm):
    datetime = DateTimeField('Дата и время:', format='%Y-%m-%dT%H:%M', default=datetime.now, validators=[DataRequired()])
    sugar_level = DecimalField('Уровень сахара:', places=1, validators=[Optional(), NumberRange(min=0, max=100, message='Введите число от 0 до 100')])
    fast_chs = DecimalField('Быстрые углеводы:', places=1, default=0)
    medium_chs = DecimalField('Средние углеводы:', places=1, default=0)
    slow_chs = DecimalField('Медленные углеводы:', places=1, default=0)
    short_insulin = DecimalField('Короткий инсулин:', places=1, default=0)
    alcohol = BooleanField('Алкоголь', default=False)
    physical_activities = DecimalField('Физическая активность (часы до окончания):', places=1, default=0)
    sleep = DecimalField('Сон (часы до окончания):', places=1, validators=[Optional(), NumberRange(min=0)])
    stress = DecimalField('Стресс (от 0 до 10):', places=1, validators=[Optional(), NumberRange(min=0, max=10)])
    changing_cannula = BooleanField('Замена канюли')
    submit = SubmitField('Отправить')
