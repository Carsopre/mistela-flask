from mistelaflask import create_app, db, models


def init_db():
    _app = create_app()
    with _app.app_context():
        # test code
        db.create_all()
