from flask import Flask
from flask_sqlalchemy import SQLAlchemy

__version__ = "0.1.0"

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    # blueprint for auth routes in our app
    from mistelaflask.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from mistelaflask.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app