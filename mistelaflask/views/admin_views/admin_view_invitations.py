from __future__ import annotations

from flask import Blueprint, Response, flash, redirect, request, url_for

from mistelaflask import db, models
from mistelaflask.utils import admin_required
from mistelaflask.views.admin_views.admin_view_base import AdminViewBase


class AdminViewInvitations(AdminViewBase):
    view_name: str = "invitations"

    @classmethod
    def register(cls, admin_blueprint: Blueprint) -> AdminViewInvitations:
        _view = cls()
        _view._add_base_url_rules(admin_blueprint)
        return _view

    @admin_required
    def _list_view(self) -> Response:
        return self._render_admin_view_template(
            "admin_invitations_list.html",
            invitations=models.UserEventInvitation.query.all(),
        )

    @admin_required
    def _detail_view(self, model_id: int) -> Response:
        return self._render_admin_view_template(
            "admin_invitations_detail.html",
            invitation=models.UserEventInvitation.query.filter_by(id=model_id).first(),
            guests=models.User.query.filter_by(admin=False).all(),
            events=models.Event.query.all(),
        )

    @admin_required
    def _remove_view(self, model_id: int) -> Response:
        models.UserEventInvitation.query.filter_by(id=model_id).delete()
        db.session.commit()
        flash(f"Invitation {model_id} has been removed.", category="danger")
        return redirect(url_for("admin.invitations_list"))

    @admin_required
    def _update_view(self, model_id: int) -> Response:
        flash("Functionality not implemented.", "danger")
        return redirect(url_for("admin.index"))

    @admin_required
    def _add_view(self) -> Response:
        return self._render_admin_view_template(
            "admin_invitations_add.html",
            invitation=models.UserEventInvitation(
                n_adults=2, n_children=0, n_babies=0, remarks=""
            ),
            guests=models.User.query.filter_by(admin=False).all(),
            events=models.Event.query.all(),
        )

    @admin_required
    def _create_view(self) -> Response:
        _sel_event_id = request.form.get("select_event")
        _sel_guest_id = request.form.get("select_guest")

        if not _sel_event_id or not _sel_guest_id:
            flash("Invalid input data")
            return redirect(url_for("admin_invitaitons_create"))
        _sel_guest_id = int(_sel_guest_id)
        _sel_event_id = int(_sel_event_id)
        _invite = models.UserEventInvitation.query.filter_by(
            user_id=_sel_guest_id, event_id=_sel_event_id
        ).first()
        if _invite:
            flash("An invite with this name already exists.", category="danger")
            return redirect(url_for("admin.invitations_create"))
        _response = request.form.get("response", None)
        if _response:
            _response = bool(_response)
        db.session.add(
            models.UserEventInvitation(
                user_id=_sel_guest_id,
                event_id=_sel_event_id,
                response=_response,
                n_adults=request.form.get("n_adults", 0),
                n_children=request.form.get("n_children", 0),
                n_babies=request.form.get("n_babies", 0),
                remarks=request.form.get("remarks", ""),
            )
        )
        db.session.commit()

        flash(
            f"Added invitation for event '{_sel_event_id}' and user '{_sel_guest_id}'.",
            category="success",
        )
        return redirect(url_for("admin.events_list"))
