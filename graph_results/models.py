from flask_login import UserMixin, current_user, login_required

from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    api_key = db.Column(db.String(1000))

class API(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    api_key = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    x = db.Column(db.String(1000))
    y = db.Column(db.String(1000))