from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from mistelaflask import db, models
from mistelaflask.views.admin_view_base import add_url_rules
from mistelaflask.views.admin_view_protocol import AdminViewProtocol


class AdminViewGuests(AdminViewProtocol):
    view_name: str = "guests"
    def _render_guests_template(self, template_name: str, **context):
        return render_template(f"admin/{self.view_name}/" + template_name, **context)

    @classmethod
    def register(cls, admin_blueprint: Blueprint) -> AdminViewGuests:
        _view = cls()
        add_url_rules(admin_blueprint, _view)
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
            guest_list.append((_guest, _invitations))

        return self._render_guests_template(
            "admin_guests_list.html", events=_events, guest_list=guest_list
        )

    @login_required
    def _detail_view(self, model_id: int):
        if not current_user.admin:
            return redirect(url_for("index"))
        _guest = models.User.query.filter_by(id=model_id).first()
        _events = models.Event.query.all()
        _invitations = []
        for _event in _events:
            _is_invited = db.session.query(
                models.UserEventInvitation.query.filter_by(
                    guest=_guest, event=_event
                ).exists()
            ).scalar()
            _invitations.append((_event, _is_invited))
        return self._render_guests_template(
            "admin_guests_detail.html", guest=_guest, invitations=_invitations
        )

    @login_required
    def _remove_view(self, model_id: int):
        if not current_user.admin:
            return redirect(url_for("index"))
        _guest: models.User = models.User.query.filter_by(id=model_id).first()
        _name = _guest.name
        models.User.query.filter_by(id=model_id).delete()
        db.session.commit()
        flash(f"User {_name} has been removed.", category="danger")
        return redirect(url_for("admin.guests_list"))

    def _set_guest_values(self, guest: models.User):
        guest.username = request.form.get("username")
        guest.name = request.form.get("name")
        guest.max_adults = request.form.get("max_adults", 2)
        guest.otp = request.form.get("otp")
        return guest

    def _set_guest_invitations(self, guest: models.User):
        for _event in models.Event.query.all():
            _form_value = True if request.form.get(f"event_{_event.name}") else False
            _exists = models.UserEventInvitation.query.filter_by(
                event=_event, guest=guest
            ).first()
            if _form_value and not _exists:
                db.session.add(models.UserEventInvitation(guest=guest, event=_event))
            elif not _form_value and _exists:
                models.UserEventInvitation.query.filter_by(
                    event=_event, guest=guest
                ).delete()
            db.session.commit()

    @login_required
    def _update_view(self, model_id: int):
        if not current_user.admin:
            return redirect(url_for("index"))
        _guest: models.User = models.User.query.filter_by(id=model_id).first()
        if not _guest:
            flash("Guest not found.", category="danger")
            return redirect(url_for("admin.guests_list"))

        self._set_guest_values(_guest)
        db.session.commit()
        self._set_guest_invitations(_guest)

        flash(f"Guest '{_guest.id}' updated", category="info")
        return redirect(url_for("admin.guests_list"))

    @login_required
    def _add_view(self):
        if not current_user.admin:
            return redirect(url_for("index"))

        _invitations = []
        for _event in models.Event.query.all():
            _invitations.append((_event, False))
        return self._render_guests_template(
            "admin_guests_add.html", guest=models.User(), invitations=_invitations
        )

    @login_required
    def _create_view(self):
        if not current_user.admin:
            return redirect(url_for("index"))

        _new_guest = models.User()
        self._set_guest_values(_new_guest)
        if models.User.query.filter_by(username=_new_guest.username).first():
            flash("A guest with this name already exists.", category="danger")
            return redirect(url_for("admin.guests_add", guest=_new_guest))
        db.session.add(_new_guest)
        db.session.commit()
        self._set_guest_invitations(_new_guest)

        flash(f"Added guest '{_new_guest.username}'.", category="success")
        return redirect(url_for("admin.guests_list"))
