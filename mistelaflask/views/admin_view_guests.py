from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash

from mistelaflask import db, models
from mistelaflask.views.admin_view_protocol import AdminViewProtocol


class AdminViewGuests(AdminViewProtocol):
    def _render_guests_template(self, template_name: str, **context):
        return render_template("admin/guests/" + template_name, **context)

    @classmethod
    def register(cls, admin_blueprint: Blueprint) -> AdminViewGuests:
        _view = cls()
        admin_blueprint.add_url_rule("/guests", "guests_list", _view._list_view)
        admin_blueprint.add_url_rule(
            "/guests/detail/<int:guest_id>",
            "guests_detail",
            _view._detail_view,
            methods=["GET"],
        )
        admin_blueprint.add_url_rule(
            "/guests/detail/<int:guest_id>",
            "guests_update",
            _view._update_view,
            methods=["POST", "PUT"],
        )
        admin_blueprint.add_url_rule(
            "/guests/remove/<int:guest_id>", "guests_remove", _view._remove_view
        )
        admin_blueprint.add_url_rule(
            "/guests/add", "guests_add", _view._add_view, methods=["GET"]
        )
        admin_blueprint.add_url_rule(
            "/guests/add", "guests_create", _view._create_view, methods=["POST"]
        )
        return _view

    @login_required
    def _list_view(self):
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

        return self._render_guests_template(
            "admin_guests.html", events=_events, guest_list=guest_list
        )

    @login_required
    def _detail_view(self, guest_id: int):
        if not current_user.admin:
            return redirect(url_for("index"))
        _guest = models.User.query.filter_by(id=guest_id).first()
        return self._render_guests_template(
            "admin_guests_detail.html",
            event=_guest,
        )

    @login_required
    def _remove_view(self, guest_id: int):
        if not current_user.admin:
            return redirect(url_for("index"))
        _guest: models.User = models.User.query.filter_by(id=guest_id).first()
        _name = _guest.name
        models.User.query.filter_by(id=guest_id).delete()
        db.session.commit()
        flash(f"User {_name} has been removed.", category="danger")
        return redirect(url_for("admin.guests_list"))

    @login_required
    def _create_view(self):
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
                _new_invitation = models.UserEventInvitation(
                    guest=_new_user, event=_event
                )
                db.session.add(_new_invitation)
                db.session.commit()
        return redirect(url_for("mistela_admin.guests"))

    @login_required
    def _update_view(self, guest_id: int):
        if not current_user.admin:
            return redirect(url_for("index"))
        _guest: models.User = models.User.query.filter_by(id=guest_id).first()
        if not _guest:
            flash("Guest not found.", category="danger")
            return redirect(url_for("admin.guests_list"))

        _guest.name = request.form.get("name")
        _guest.description = request.form.get("description")
        db.session.commit()
        flash(f"Guest '{_guest.id}' updated", category="info")
        return redirect(url_for("admin.guests_list"))

    @login_required
    def _add_view(self):
        if not current_user.admin:
            return redirect(url_for("index"))
        return self._render_guests_template("admin_guests_add.html")

    @login_required
    def _create_view(self):
        if not current_user.admin:
            return redirect(url_for("index"))
        name = request.form.get("name")
        description = request.form.get("description")

        _guest = models.User.query.filter_by(name=name).first()
        if _guest:
            flash("A guest with this name already exists.", category="danger")
            return redirect(url_for("guests_create"))
        _new_guest = models.User(name=name, description=description)
        db.session.add(_new_guest)
        db.session.commit()
        flash(f"Added guest '{name}'.", category="success")
        return redirect(url_for("admin.guests_list"))
