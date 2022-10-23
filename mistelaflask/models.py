from flask_login import UserMixin

from mistelaflask import db


class User(UserMixin, db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    name = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean, default=False, nullable=False)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    description = db.Column(db.Text)


class UserInvitation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    remarks = db.Column(db.Text)


class UserEventInvitation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest = db.Column(db.Integer, db.ForeignKey("user.id"))
    event = db.Column(db.Integer, db.ForeignKey("event.id"))
    response = db.Column(db.Boolean, default=False, nullable=False)
