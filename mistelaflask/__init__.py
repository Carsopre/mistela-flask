import os

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# set optional bootswatch theme
__version__ = "0.4.0"

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

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from mistelaflask.models import Event, User, UserEventInvitation

    # app.config["FLASK_ADMIN_SWATCH"] = "cerulean"
    # admin = Admin(app, name="microblog", template_mode="bootstrap4")
    # admin.add_view(ModelView(User, db.session))
    # admin.add_view(ModelView(Event, db.session))
    # admin.add_view(ModelView(UserEventInvitation, db.session))

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
