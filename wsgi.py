import os
import secrets
from datetime import datetime
from pathlib import Path

import pip

try:
    # pip.main(["install", "mistela-flask"])
    _current_dir = Path(__file__).parent
    pip.main(["install", _current_dir])
except Exception as e_info:
    pass


from werkzeug.security import generate_password_hash

from mistelaflask import Flask, create_app, db, models


def init_test_db() -> Flask:
    _app = create_app()
    if "sqlite" in os.environ["DATABASE_URI"]:
        _db_file = Path(__file__).parent / "instance" / "db.sqlite"
        _db_file.unlink(missing_ok=True)

    with _app.app_context():
        db.create_all()
        admin = models.User(
            username="admin",
            password=generate_password_hash("admin", method="sha256"),
            admin=True,
        )
        db.session.add(admin)
        # All day guest
        _day_guest = models.User(
            username="dayguest",
            name="Day Guest",
            otp="1234",
            admin=False,
            max_adults=2,
        )
        _night_guest = models.User(
            username="nightguest",
            name="Night Guest",
            otp="5678",
            admin=False,
            max_adults=2,
        )
        db.session.add(_day_guest)
        db.session.add(_night_guest)
        db.session.commit()

        wedding_date = datetime(2023, 5, 20, 16, 0, 0)

        def _correct_datetime(**kwargs):
            return wedding_date.replace(**kwargs)

        events = [
            models.Event(
                name="reception",
                icon="fa fa-signs-post",
                start_time=_correct_datetime(hour=16, minute=00),
                duration=30,
                description="Guests can gather at the venue and enjoy a welcome drink.",
            ),
            models.Event(
                name="ceremony",
                icon="fa fa-ring fa-rotate-90",
                start_time=_correct_datetime(hour=16, minute=30),
                duration=45,
                description="Wedding ceremony with ring exchange.",
            ),
            models.Event(
                name="cake and toast",
                icon="fa fa-champagne-glasses",
                start_time=_correct_datetime(hour=17, minute=15),
                duration=75,
                description="A toast with cava and cake to celebrate the moment.",
            ),
            models.Event(
                name="dinner",
                icon="fa fa-utensils",
                description="BBQ Buffet with dessert table.",
                start_time=_correct_datetime(hour=18, minute=30),
                duration=150,
            ),
            models.Event(
                name="party",
                icon="fa fa-music",
                description="We will play some musice to dance and finish the day with a warm party",
                start_time=_correct_datetime(hour=21),
                duration=4 * 60,
            ),
        ]

        for _event in events:
            db.session.add(_event)
            db.session.commit()
            _invitation = models.UserEventInvitation(
                guest_id=_day_guest.id, event_id=_event.id
            )
            db.session.add(_invitation)
        _night_invitation = models.UserEventInvitation(
            guest_id=_night_guest.id, event_id=events[-1].id
        )
        db.session.add(_night_invitation)
        db.session.commit()
        return _app


os.environ["SECRET_KEY"] = secrets.token_hex(16)  # Required environment variable.
os.environ["DATABASE_URI"] = "sqlite:///db.sqlite"
app = init_test_db()
