import datetime
import os

from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# set optional bootswatch theme
__version__ = "0.9.0"

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
default_database_uri = "sqlite:///db.sqlite"
admin: Admin = None


def create_app() -> Flask:
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URI", default_database_uri
    )
    db.init_app(app)

    @app.context_processor
    def inject_general_variables():
        return dict(version=__version__)

    @app.template_filter()
    def format_datetime(date_value: datetime.datetime, strftime_format: str) -> str:
        return date_value.strftime(strftime_format)

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
    from mistelaflask.views.admin_views import admin_view as admin_blueprint

    app.register_blueprint(admin_blueprint)

    from mistelaflask.views.guest_views import main_view as guest_blueprint

    app.register_blueprint(guest_blueprint)
    return app
