![GitHub release (latest by date)](https://img.shields.io/github/v/release/carsopre/mistela-flask)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/carsopre/mistela-flask)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# mistela-flask
A multi-event planner elaborated with Flask

Initial steps done following this [Digital Ocean guide](https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login#step-7-setting-up-the-authorization-function)

## Usage
Mistela-flask can be used as a package and easily deployed as any regular flask app.
```python
from mistelaflask import create_app
import secrets
import os
os.environ["SECRET_KEY"] = secrets.token_hex(16) # Required environment variable.
os.environ["DATABASE_URI"] = "sqlite:///db.sqlite"
app = create_app() 
app.run()
```
> By default, mistelaflask will run on a `SQLite` database.

A more detailed example can be found in the root of the repository as `wsgi.py`.

## Installing the repository.
To develop on the repository you should be using `Poetry`. Once installed, simply run the install command `poetry install` and all development and production dependencies will be added to your virtual environment.
