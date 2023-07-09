from sqlalchemy import event
from app.database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(250))
    sugar_data = db.relationship('SugarData', back_populates="user")
    basal_intervals = db.relationship('Basal', back_populates="user")

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

class SugarData(db.Model):
    __tablename__ = 'sugar_data'
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)
    sugar_level = db.Column(db.Float)
    basal_insulin = db.Column(db.Integer, db.ForeignKey('basal_intervals.id'))
    fast_chs = db.Column(db.Float)
    medium_chs = db.Column(db.Float)
    slow_chs = db.Column(db.Float)
    short_insulin = db.Column(db.Float)
    alcohol = db.Column(db.Float)
    physical_activities = db.Column(db.Float)
    sleep = db.Column(db.Float)
    stress = db.Column(db.Float)
    changing_cannula = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates="sugar_data")

    def __init__(self, datetime, sugar_level, basal_insulin, fast_chs, medium_chs, slow_chs, short_insulin, alcohol, physical_activities, sleep, stress, changing_cannula, user_id):
        self.datetime = datetime
        self.sugar_level = sugar_level
        self.basal_insulin = basal_insulin
        self.fast_chs = fast_chs
        self.medium_chs = medium_chs
        self.slow_chs = slow_chs
        self.short_insulin = short_insulin
        self.alcohol = alcohol
        self.physical_activities = physical_activities
        self.sleep = sleep
        self.stress = stress
        self.changing_cannula = changing_cannula
        self.user_id = user_id

class Basal(db.Model):
    __tablename__ = 'basal_intervals'
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)
    interval_num = db.Column(db.Integer)
    basal_insulin = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates="basal_intervals")

    def __init__(self, datetime, interval_num, basal_insulin, user_id):
        self.datetime = datetime
        self.interval_num = interval_num
        self.basal_insulin = basal_insulin
        self.user_id = user_id
