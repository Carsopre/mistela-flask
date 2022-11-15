from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required

from mistelaflask import models
from mistelaflask.views.admin_view_events import AdminViewEvents
from mistelaflask.views.admin_view_guests import AdminViewGuests

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/")
@login_required
def index():
    if not current_user.admin:
        return redirect(url_for("main.index"))
    return render_template("admin/admin_index.html")


def render_guests_template(template_name: str, **context):
    return render_template("admin/guests/" + template_name, **context)


event_view = AdminViewEvents.register(admin)
guest_view = AdminViewGuests.register(admin)


@admin.route("/responses")
@login_required
def responses():
    if not current_user.admin:
        return redirect(url_for("index"))

    _events = models.Event.query.all()
    _user_list = []
    for _guest in models.User.query.filter_by(admin=False):
        _user_list.append(
            dict(
                name=_guest.name,
                max_adults=_guest.max_adults,
                invitations=[
                    models.UserEventInvitation.query.filter_by(
                        guest=_guest, event=_event
                    )
                    for _event in _events
                ],
            )
        )
    return render_template(
        "admin/admin_responses.html", events=_events, guest_list=_user_list
    )
