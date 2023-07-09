from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

db = SQLAlchemy()
from sqlalchemy.exc import SQLAlchemyError

from app.mainmodule.models import User

'''User'''

def get_user_by_id(user_id):
    try:
        user = User.query.get(user_id)
        return {"status": 200, "message": 'User found', "result": user}
    except SQLAlchemyError:
        return {"status": 500, "message": "Error occurred while getting user", "result": None}

def check_user_email_exists(email):
    try:
        user_existing = bool(User.query.filter_by(email=email).first())
        message = "User exists" if user_existing else "User does not exist"
        return {"status": 200, "message": message, "result": user_existing}
    except SQLAlchemyError:
        return {"status": 500, "message": "Error occurred while checking email existence", "result": None}


from werkzeug.security import generate_password_hash, check_password_hash

def check_user_entered_data(email, password):
    try:
        user = User.query.filter(email == email).first()

        if user and check_password_hash(user.password, password):
            return {"status": 200, "message": "Login successful", "result": user.id}
        else:
            return {"status": 401, "message": "Invalid email or password", "result": None}
    except SQLAlchemyError:
        return {"status": 500, "message": "Error occurred while checking user data", "result": None}

def register_new_user(first_name, last_name, email, password):
    try:
        user = User(first_name=first_name, last_name=last_name, email=email, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        if user.id:
            return {"status": 200, "message": "User registered successfully", "result": user.id}
        else:
            return {"status": 401, "message": "Failed to register user", "result": None}
    except SQLAlchemyError:
        return {"status": 500, "message": "Error occurred while registering new user", "result": None}

from app.mainmodule.models import Basal

''' Basal '''

def create_modify_basal(datetime, interval_num, basal_insulin, user_id):
    try:
        basal = Basal.query.filter_by(interval_num=interval_num, basal_insulin=basal_insulin).first()
        if basal:
            basal.datetime = datetime
            db.session.commit()
            return {"status": 200, "message": "Basal record already exists. Datetime updated", "result": basal.id}
        basal = Basal(datetime=datetime, interval_num=interval_num, basal_insulin=basal_insulin, user_id=user_id)
        db.session.add(basal)
        db.session.commit()
        return {"status": 200, "message": "Basal record created", "result": basal.id}
    except SQLAlchemyError:
        return {"status": 500, "message": "Error occurred while creating/modifying basal record"}

from app.mainmodule.models import SugarData

''' SugarData'''

def add_sugar_data(datetime, sugar_level, basal_insulin, fast_chs, medium_chs, slow_chs, short_insulin, alcohol, physical_activities, sleep, stress, changing_cannula, user_id):
    try:
        sugar_data = SugarData(datetime=datetime, sugar_level=sugar_level, basal_insulin=basal_insulin, user_id=user_id)
        db.session.add(sugar_data)
        db.session.commit()
        return {"status": 200, "message": "Sugar data record added", "result": sugar_data.id}
    except SQLAlchemyError:
        return {"status": 500, "message": "Error occurred while adding sugar data record"}
