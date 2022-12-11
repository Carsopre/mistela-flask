import os
import secrets
from datetime import datetime
from pathlib import Path

# Work with the development environment
# add your project directory to the sys.path
_dev_mistela_app = Path(__file__).parent / "mistelaflask"
if _dev_mistela_app.is_dir():
    import sys

    if _dev_mistela_app not in sys.path:
        sys.path = [_dev_mistela_app] + sys.path

from mistelaflask import Flask, create_app, db, models


def init_mistelaflask():
    def init_test_db() -> Flask:
        _app = create_app()
        if "sqlite" in os.environ["DATABASE_URI"]:
            _db_file = Path(__file__).parent / "instance" / "db.sqlite"
            if not _db_file.is_file():
                with _app.app_context():
                    db.create_all()
                    admin = models.User(
                        username="admin",
                        otp="1234",
                        admin=True,
                    )
                    db.session.add(admin)
                    db.session.commit()
            return _app

    os.environ["SECRET_KEY"] = secrets.token_hex(16)  # Required environment variable.
    os.environ["DATABASE_URI"] = "sqlite:///db.sqlite"
    os.environ["MISTELA_TITLE"] = "My big event"
    os.environ["STATIC_FOLDER"] = "path//to//my//static//folder"
    os.environ["MAIL_USERNAME"] = "joe.doe@email.com"
    os.environ["MAIL_PASSWORD"] = "1234"
    return init_test_db()


app = init_mistelaflask()
