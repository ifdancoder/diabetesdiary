from ..database import check_user_email_exists
from wtforms import validators

def existing_email(message=None):
    if message == None:
        message = "Пользователь с таким email уже существует"
    def _existing_email(form, email):
        api_res = check_user_email_exists(email.data)
        if api_res['result']:
            raise validators.ValidationError(message)
    return _existing_email
