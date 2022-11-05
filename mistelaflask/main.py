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


@main.route("/responses")
@login_required
def responses():
    # current_user
    _user_invitations = []
    for _invitation in models.UserEventInvitation.query.filter_by(
        guest=current_user.id
    ):
        _event = models.Event.query.filter_by(id=_invitation.id).first()
        _user_invitations.append(
            dict(
                event_name=_event.name,
                max_adults=current_user.max_adults,
            )
        )

    return render_template("guest_responses.html", user_invitations=_user_invitations)


@main.route("/responses", methods=["UPDATE"])
@login_required
def update_responses():
    pass
