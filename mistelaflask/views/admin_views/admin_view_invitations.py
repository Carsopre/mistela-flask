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
        admin_blueprint.add_url_rule(
            f"/{_view.view_name}/summary/",
            f"{_view.view_name}_summary",
            _view._summary_view,
        )
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

    @admin_required
    def _summary_view(self) -> Response:
        class SummaryModel:
            event: models.Event
            t_adults: int
            t_children: int
            t_babies: int

        _summary_events = []

        def get_summary(
            event: models.Event, adults: int, children: int, babies: int
        ) -> SummaryModel:
            _summary = SummaryModel()
            _summary.event = event
            _summary.t_adults = adults
            _summary.t_children = children
            _summary.t_babies = babies
            return _summary

        for _event in models.Event.query.all():
            _invitations = models.UserEventInvitation.query.filter_by(
                event_id=_event.id
            )
            _tuples = [
                (_inv.n_adults, _inv.n_children, _inv.n_babies)
                for _inv in _invitations
                if _inv.response
            ]
            _t_adults = _t_children = _t_babies = 0
            if _tuples:
                _t_adults, _t_children, _t_babies = sum(_tuples)

            _summary_events.append(
                get_summary(_event, _t_adults, _t_children, _t_babies)
            )
        return self._render_admin_view_template(
            "admin_invitations_summary.html", summaries=_summary_events
        )
