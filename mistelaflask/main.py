from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from mistelaflask import db, models

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.name)


@main.route("/events")
@login_required
def events():
    _events = models.Event.query.all()
    return render_template("events.html", events=_events)
