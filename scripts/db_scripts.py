from pathlib import Path

from requests import session
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
        event_names = ["ceremony", "cake", "dinner", "party"]
        list(map(lambda x: db.session.add(models.Event(name=x)), event_names))
        db.session.commit()
