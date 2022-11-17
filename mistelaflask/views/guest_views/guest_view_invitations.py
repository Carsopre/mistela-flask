from __future__ import annotations

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from mistelaflask import db, models
from mistelaflask.views.guest_views.guest_view_protocol import GuestViewProtocol


class GuestViewInvitations(GuestViewProtocol):
    view_name: str = "invitations"

    def _render_guest_view_template(self, template_name: str, **context):
        return render_template(f"guest/" + template_name, **context)

    @classmethod
    def register(cls, guest_blueprint: Blueprint) -> GuestViewInvitations:
        _view = cls()
        guest_blueprint.add_url_rule(
            "/invitations/", "invitations_list", _view._list_view, methods=["GET"]
        )
        guest_blueprint.add_url_rule(
            "/invitations/",
            "invitations_bulk_update",
            _view._bulk_update_view,
            methods=["POST", "PUT"],
        )
        return _view

    @login_required
    def _list_view(self):
        # current_user
        return self._render_guest_view_template(
            "guest_invitations.html",
            user_invitations=models.UserEventInvitation.query.filter_by(
                guest_id=current_user.id
            ),
        )

    @login_required
    def _bulk_update_view(self):
        for _inv in models.UserEventInvitation.query.filter_by(guest=current_user.id):
            _response = request.form.get("response", None)
            if _response:
                _response = _response.lower() == "true"
            else:
                _response = None
            _inv.response = _response
            _inv.n_adults = min(
                int(request.form.get(f"{_inv.id}_n_adults", _inv.n_adults)),
                _inv.guest.max_adults,
            )
            _inv.n_children = int(
                request.form.get(f"{_inv.id}_n_children", _inv.n_children)
            )
            _inv.n_babies = int(request.form.get(f"{_inv.id}_n_babies", _inv.n_babies))
            _inv.remarks = request.form.get(f"{_inv.id}_remarks", _inv.remarks)
            db.session.add(_inv)
            db.session.commit()
        return redirect(url_for("main.invitations_list"))
