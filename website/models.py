from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Text(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    context = db.Column(db.String(20000), unique = True)
    count = db.Column(db.Integer)###

class Label(db.Model):
    label = db.Column(db.String(150), primary_key = True)

class LabelingInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(150), db.ForeignKey('label.label'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.String(10000))#, db.ForeignKey('text.context'))
    date = db.Column(db.DateTime(timezone = True), default = func.now())
    
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    state = db.Column(db.Boolean)
    labels = db.relationship('LabelingInfo')
    