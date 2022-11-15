from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from mistelaflask import db, models

admin = Blueprint("admin", __name__)


@admin.route("/admin/")
@login_required
def index():
    if not current_user.admin:
        return redirect(url_for("main.index"))
    return render_template("admin/admin_index.html")


def render_events_template(template_name: str, **context):
    return render_template("admin/events/" + template_name, **context)


def render_guests_template(template_name: str, **context):
    return render_template("admin/guests/" + template_name, **context)


@admin.route("/admin/events")
@login_required
def events():
    if not current_user.admin:
        return redirect(url_for("index"))
    _events = models.Event.query.all()
    return render_events_template("admin_events_list.html", events=_events)


@admin.route("/admin/events/detail/<int:event_id>", methods=["GET"])
@login_required
def events_detail(event_id: int):
    if not current_user.admin:
        return redirect(url_for("index"))
    _event = models.Event.query.filter_by(id=event_id).first()
    return render_events_template(
        "admin_events_detail.html",
        event=_event,
    )


@admin.route("/admin/events/remove/<int:event_id>", methods=["GET"])
@login_required
def events_remove(event_id: int):
    if not current_user.admin:
        return redirect(url_for("index"))
    _event: models.Event = models.Event.query.filter_by(id=event_id).first()
    _name = _event.name
    models.Event.query.filter_by(id=event_id).delete()
    db.session.commit()
    flash(f"Event {_name} has been removed.")
    return redirect(url_for("admin.events"))


@admin.route("/admin/events/add", methods=["GET"])
def events_add():
    if not current_user.admin:
        return redirect(url_for("index"))
    return render_events_template("admin_events_add.html")


@admin.route("/admin/events/add", methods=["POST"])
@login_required
def events_create():
    if not current_user.admin:
        return redirect(url_for("index"))
    name = request.form.get("name")
    description = request.form.get("description")

    _event = models.Event.query.filter_by(name=name).first()
    if _event:
        flash("An event with this name already exists.")
        return redirect(url_for("events"))
    _new_event = models.Event(name=name, description=description)
    db.session.add(_new_event)
    db.session.commit()
    return redirect(url_for("mistela_admin.events"))


@admin.route("/admin/guests")
@login_required
def guests():
    class GuestInvitation:
        invited: bool

    if not current_user.admin:
        return redirect(url_for("index"))
    _events = models.Event.query.all()
    guest_list = []
    for _guest in models.User.query.filter_by(admin=False):
        _invitations = []
        for _event in _events:
            gi = GuestInvitation()
            gi.invited = db.session.query(
                models.UserEventInvitation.query.filter_by(
                    guest=_guest, event=_event
                ).exists()
            ).scalar()
            gi.event = _event
            _invitations.append(gi)

        guest_list.append(
            dict(
                guest_id=_guest.id,
                name=_guest.name,
                max_adults=_guest.max_adults,
                invitations=_invitations,
            )
        )

    return render_guests_template(
        "admin_guests.html", events=_events, guest_list=guest_list
    )


@admin.route("/admin/guests/add", methods=["POST"])
@login_required
def create_guest_post():
    if not current_user.admin:
        return redirect(url_for("index"))
    name = request.form.get("name")
    password = request.form.get("password")
    max_adults = request.form.get("max_adults")
    _user = models.User.query.filter_by(name=name).first()
    if _user:
        flash("A user with this name already exists.")
        return redirect(url_for("mistela_admin.guests"))
    _new_user = models.User(
        name=name,
        max_adults=max_adults,
        password=generate_password_hash(password, method="sha256"),
    )
    db.session.add(_new_user)
    db.session.commit()
    _user_invitation = models.UserEventInvitation(guest=_new_user.id)
    db.session.add(_user_invitation)
    db.session.commit()
    for _event in models.Event.query.all():
        if request.form.get(f"event_{_event.id}", type=bool, default=False):
            _new_invitation = models.UserEventInvitation(guest=_new_user, event=_event)
            db.session.add(_new_invitation)
            db.session.commit()
    return redirect(url_for("mistela_admin.guests"))


@admin.route("/admin/guests/<int:guest_id>", methods=["POST"])
@login_required
def update_guest(guest_id: int):
    pass


@admin.route("/admin/responses")
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
