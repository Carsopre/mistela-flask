from __future__ import annotations

from flask import Blueprint, flash, redirect, request, url_for

from mistelaflask import db, models
from mistelaflask.utils import admin_required
from mistelaflask.views.admin_views.admin_view_base import AdminViewBase


class AdminViewGuests(AdminViewBase):
    view_name: str = "guests"

    @classmethod
    def register(cls, admin_blueprint: Blueprint) -> AdminViewGuests:
        _view = cls()
        _view._add_base_url_rules(admin_blueprint)
        admin_blueprint.add_url_rule(
            f"/{_view.view_name}/add/batch/",
            f"{_view.view_name}_add_batch",
            _view._add_batch_view,
            methods=["GET"],
        )
        admin_blueprint.add_url_rule(
            f"/{_view.view_name}/add/batch/",
            f"{_view.view_name}_create_batch",
            _view._create_batch_view,
            methods=["POST"],
        )
        return _view

    @admin_required
    def _list_view(self):
        class GuestInvitation:
            invited: bool

        _events = models.Event.query.all()
        guest_list = []
        for _guest in models.User.query.filter_by():
            _invitations = []
            for _event in _events:
                gi = GuestInvitation()
                gi.invited = db.session.query(
                    models.UserEventInvitation.query.filter_by(
                        guest_id=_guest.id, event_id=_event.id
                    ).exists()
                ).scalar()
                gi.event = _event
                _invitations.append(gi)
            guest_list.append((_guest, _invitations))

        return self._render_admin_view_template(
            "admin_guests_list.html", events=_events, guest_list=guest_list
        )

    @admin_required
    def _detail_view(self, model_id: int):
        _guest = models.User.query.filter_by(id=model_id).first()
        _events = models.Event.query.all()
        _invitations = []
        for _event in _events:
            _is_invited = db.session.query(
                models.UserEventInvitation.query.filter_by(
                    event_id=_event.id, guest_id=_guest.id
                ).exists()
            ).scalar()
            _invitations.append((_event, _is_invited))
        return self._render_admin_view_template(
            "admin_guests_detail.html", guest=_guest, invitations=_invitations
        )

    @admin_required
    def _remove_view(self, model_id: int):
        _guest: models.User = models.User.query.filter_by(id=model_id).first()
        _name = _guest.name
        models.User.query.filter_by(id=model_id).delete()
        models.UserEventInvitation.query.filter_by(guest_id=model_id).delete()
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
                event_id=_event.id, guest_id=guest.id
            ).first()
            if _form_value and not _exists:
                db.session.add(
                    models.UserEventInvitation(guest_id=guest.id, event=_event.id)
                )
            elif not _form_value and _exists:
                models.UserEventInvitation.query.filter_by(
                    event_id=_event.id, guest_id=guest.id
                ).delete()
            db.session.commit()

    @admin_required
    def _update_view(self, model_id: int):
        _guest: models.User = models.User.query.filter_by(id=model_id).first()
        if not _guest:
            flash("Guest not found.", category="danger")
            return redirect(url_for("admin.guests_list"))

        self._set_guest_values(_guest)
        db.session.commit()
        self._set_guest_invitations(_guest)

        flash(f"Guest '{_guest.id}' updated", category="info")
        return redirect(url_for("admin.guests_list"))

    @admin_required
    def _add_view(self):
        _invitations = []
        for _event in models.Event.query.all():
            _invitations.append((_event, False))
        return self._render_admin_view_template(
            "admin_guests_add.html", guest=models.User(), invitations=_invitations
        )

    @admin_required
    def _create_view(self):
        _new_guest = models.User()
        self._set_guest_values(_new_guest)
        if models.User.query.filter_by(username=_new_guest.username).first():
            flash("A guest with this name already exists.", category="danger")
            return redirect(url_for("admin.guests_add"))
        db.session.add(_new_guest)
        db.session.commit()
        self._set_guest_invitations(_new_guest)

        flash(f"Added guest '{_new_guest.username}'.", category="success")
        return redirect(url_for("admin.guests_list"))

    @admin_required
    def _add_batch_view(self):
        return self._render_admin_view_template(
            "admin_guests_add_batch.html", events=models.Event.query.all()
        )

    @admin_required
    def _create_batch_view(self):
        _names_list = request.form.get("names_list", "")

        # Extract other properties
        _max_adults = request.form.get("max_adults", 2, type=int)
        _otp = request.form.get("otp")

        # Extract invitations
        _invitations = []
        for _event in models.Event.query.all():
            _invited = True if request.form.get(f"event_{_event.name}") else False
            if _invited:
                _invitations.append(_event)

        for _idx, name in enumerate(_names_list.splitlines()):
            _full_name = name.strip()
            _username = _full_name[0:3] + _full_name[-4:-1]
            if models.User.query.filter_by(username=_username).first():
                _username = _username + str(_idx)
            _user = models.User(
                username=_username,
                name=_full_name,
                otp=_otp,
                admin=False,
                max_adults=_max_adults,
            )
            db.session.add(_user)
            db.session.commit()
            db.session.refresh(_user)

            for _event_invite in _invitations:
                db.session.add(
                    models.UserEventInvitation(
                        event_id=_event_invite.id, guest_id=_user.id
                    )
                )
                db.session.commit()

        return redirect(url_for("admin.guests_list"))
