![GitHub release (latest by date)](https://img.shields.io/github/v/release/carsopre/mistela-flask)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/carsopre/mistela-flask)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# mistela-flask
A multi-event planner elaborated with Flask.

Initial steps done following this [Digital Ocean guide](https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login#step-7-setting-up-the-authorization-function)

This version of `Flask` aims to provide a simpile solution to manage an event such as a wedding with different 'sub-events'. The tool also provides a custom-defined admin page as `Flask` does not really provide one itself (and I did not like `Flask-admin` as all users seemed to have admin rights).

Either way, this was a nice user-case for me to get hands-on with Flask.

## Why the name Mistela?
Mistela is 'sort of a wine' quite common in my region (València, Spain) for celebrations or simply after a family dinner. It made sense that if this flask 'flavour' is about events (celebrations) management, it should have an appropiate name, therefore, mistela-flask :).

## Downloading the package.
For the moment only github is available as package manager, to download the package:
```cli
pip install git+https://github.com/Carsopre/mistela-flask.git
```

## Installing the repository.
To develop on the repository you should be using `Poetry`. Once installed, simply run the install command `poetry install` and all development and production dependencies will be added to your virtual environment.

## Usage
Mistela-flask can be used as a package and easily deployed as any regular flask app.
```python
from mistelaflask import create_app
import secrets
import os
os.environ["SECRET_KEY"] = secrets.token_hex(16) # Required environment variable.
os.environ["DATABASE_URI"] = "sqlite:///db.sqlite"
os.environ["MISTELA_TITLE"] = "My big event"
os.environ["STATIC_FOLDER"] = "path//to//my//static//folder"
os.environ["MAIL_USERNAME"] = "joe.doe@email.com"
os.environ["MAIL_PASSWORD"] = "1234"

app = create_app() 
app.run()
```
> By default, mistelaflask will run on a `SQLite` database.

A more 'real' example can be found in the root of the repository as `wsgi.py`.


