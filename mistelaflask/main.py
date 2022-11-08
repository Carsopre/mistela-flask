from datetime import timedelta

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from mistelaflask import db, models

main = Blueprint("main", __name__)


@main.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))

    _events = []
    for _invitation in models.UserEventInvitation.query.filter_by(
        guest=current_user.id
    ):
        _event = models.Event.query.filter_by(id=_invitation.event).first()
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
        _event = models.Event.query.filter_by(id=_invitation.event).first()
        _user_invitations.append(
            dict(
                event_name=_event.name,
                max_adults=current_user.max_adults,
                response=_invitation.response,
                remarks=_invitation.remarks,
                n_adults=_invitation.n_adults,
                n_children=_invitation.n_children,
            )
        )

    return render_template("guest_responses.html", user_invitations=_user_invitations)


@main.route("/responses/", methods=["POST"])
@login_required
def update_responses():
    for _invitation in models.UserEventInvitation.query.filter_by(
        guest=current_user.id
    ):
        _event = models.Event.query.filter_by(id=_invitation.event).first()
        _invitation.response = (
            True if request.form.get(f"{_event.name}_accepted") else False
        )
        # _invitation.n_adults = min(
        #     current_user.max_adults,
        #     int(
        #         request.form.get(
        #             f"{_event.name}_total_adults", str(_invitation.n_adults)
        #         )
        #     ),
        # )
        # _invitation.n_children = int(
        #     request.form.get(f"{_event.name}_total_children", _invitation.n_children)
        # )
        _invitation.remarks = request.form.get(f"{_event.name}_remarks", "")
        db.session.add(_invitation)
        db.session.commit()
    return redirect(url_for("main.responses"))
