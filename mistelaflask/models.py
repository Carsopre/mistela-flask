from flask_login import UserMixin

from mistelaflask import db


class User(UserMixin, db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    username = db.Column(db.String(1000), unique=True)
    name = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean, default=False, nullable=False)
    max_adults = db.Column(db.Integer, default=2)
    otp = db.Column(db.String(100))

    def __str__(self) -> str:
        return self.name


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    description = db.Column(db.Text)
    url_link = db.Column(db.String(1000))


class MainEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    description = db.Column(db.Text)
    contact = db.Column(db.Text)

    # Relationships
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    location = db.relationship(
        "Location",
        backref=db.backref("location_main_events", lazy="dynamic"),
    )


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    icon = db.Column(db.String(1000))
    name = db.Column(db.String(1000))
    start_time = db.Column(db.DateTime)
    duration = db.Column(db.Integer)  # In Minutes
    description = db.Column(db.Text)

    # Relationships
    main_event_id = db.Column(db.Integer, db.ForeignKey("main_event.id"))
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"))

    main_event = db.relationship(
        "MainEvent",
        backref=db.backref("main_event_events", lazy="dynamic"),
    )

    def __str__(self) -> str:
        return self.name


class UserEventInvitation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
    response = db.Column(db.Boolean, default=None, nullable=True)
    n_adults = db.Column(db.Integer, default=0)
    n_children = db.Column(db.Integer, default=0)
    n_babies = db.Column(db.Integer, default=0)
    remarks = db.Column(db.String(1000))

    guest = db.relationship(
        "User",
        backref=db.backref("guest_invitations", lazy="dynamic"),
    )
    event = db.relationship("Event", backref=db.backref("event_guests", lazy="dynamic"))
