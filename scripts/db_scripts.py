from datetime import datetime
from pathlib import Path

from werkzeug.security import generate_password_hash

from mistelaflask import create_app, db, models


def init_db():
    _app = create_app()
    with _app.app_context():
        # test code
        db.create_all()


def create_test_admin():
    _app = create_app()
    with _app.app_context():
        admin = models.User(
            name="admin",
            password=generate_password_hash("admin", method="sha256"),
            admin=True,
        )
        db.session.add(admin)
        db.session.commit()


def init_test_db():
    _app = create_app()
    _db_file = Path(__file__).parent.parent / "instance" / "db.sqlite"
    if _db_file.is_file():
        _db_file.unlink()
    with _app.app_context():
        db.create_all()
        admin = models.User(
            name="admin",
            password=generate_password_hash("admin", method="sha256"),
            admin=True,
        )
        db.session.add(admin)
        # All day guest
        _day_guest = models.User(
            name="day_guest",
            password=generate_password_hash("day_guest", method="sha256"),
            admin=False,
            max_adults=2,
        )
        _night_guest = models.User(
            name="night_guest",
            password=generate_password_hash("night_guest", method="sha256"),
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
                start_time=_correct_datetime(hour=16, minute=00),
                duration=30,
                description="Guests can gather at the venue and enjoy a welcome drink.",
            ),
            models.Event(
                name="ceremony",
                start_time=_correct_datetime(hour=16, minute=30),
                duration=45,
                description="Wedding ceremony with ring exchange.",
            ),
            models.Event(
                name="cake and toast",
                start_time=_correct_datetime(hour=17, minute=15),
                duration=75,
                description="A toast with cava and cake to celebrate the moment.",
            ),
            models.Event(
                name="dinner",
                description="BBQ Buffet with dessert table.",
                start_time=_correct_datetime(hour=18, minute=30),
                duration=150,
            ),
            models.Event(
                name="party",
                description="We will play some musice to dance and finish the day with a warm party",
                start_time=_correct_datetime(hour=21),
                duration=4 * 60,
            ),
        ]

        for _event in events:
            db.session.add(_event)
            db.session.commit()
            _invitation = models.UserEventInvitation(
                guest=_day_guest.id, event=_event.id
            )
            db.session.add(_invitation)
        _night_invitation = models.UserEventInvitation(
            guest=_night_guest.id, event=events[-1].id
        )
        db.session.add(_night_invitation)

        db.session.commit()
