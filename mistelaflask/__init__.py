import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

__version__ = "0.3.0"

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
default_database_uri = "sqlite:///db.sqlite"


def create_app() -> Flask:
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URI", default_database_uri
    )

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from mistelaflask.models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from mistelaflask.auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from mistelaflask.admin import admin as admin_blueprint

    app.register_blueprint(admin_blueprint)

    from mistelaflask.main import main as main_blueprint

    app.register_blueprint(main_blueprint)
    return app
