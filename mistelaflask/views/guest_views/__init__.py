from datetime import timedelta

from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user

from mistelaflask import models
from mistelaflask.views.guest_views.guest_events_invitations import GuestViewEvents
from mistelaflask.views.guest_views.guest_view_invitations import GuestViewInvitations

main_view = Blueprint("main", __name__)


@main_view.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))

    _events = []
    for _invitation in models.UserEventInvitation.query.filter_by(guest=current_user):
        _event = models.Event.query.filter_by(id=_invitation.event.id).first()
        _events.append(_event)
    _events.sort(key=(lambda x: x.start_time))

    def _transform(event) -> dict:
        return dict(
            start_time=event.start_time.strftime("%H:%M"),
            end_time=(event.start_time + timedelta(minutes=event.duration)).strftime(
                "%H:%M"
            ),
            name=event.name,
            description=event.description,
        )

    return render_template("index.html", timeline=list(map(_transform, _events)))


invitations_view = GuestViewInvitations.register(main_view)
events_view = GuestViewEvents.register(main_view)
