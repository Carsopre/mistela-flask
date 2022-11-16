from __future__ import annotations

from flask import (
    Blueprint,
    Response,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

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
        flash("Functionality not implemented.", "danger")
        return redirect(url_for("admin.index"))

    @admin_required
    def _detail_view(self, model_id: int) -> Response:
        flash("Functionality not implemented.", "danger")
        return redirect(url_for("admin.index"))

    @admin_required
    def _remove_view(self, model_id: int) -> Response:
        flash("Functionality not implemented.", "danger")
        return redirect(url_for("admin.index"))

    @admin_required
    def _update_view(self, model_id: int) -> Response:
        flash("Functionality not implemented.", "danger")
        return redirect(url_for("admin.index"))

    @admin_required
    def _add_view(self) -> Response:
        flash("Functionality not implemented.", "danger")
        return redirect(url_for("admin.index"))

    @admin_required
    def _create_view(self) -> Response:
        flash("Functionality not implemented.", "danger")
        return redirect(url_for("admin.index"))


# @admin.route("/responses")
# @admin_required
# def responses():
#     if not current_user.admin:
#         return redirect(url_for("index"))

#     _events = models.Event.query.all()
#     _user_list = []
#     for _guest in models.User.query.filter_by(admin=False):
#         _user_list.append(
#             dict(
#                 name=_guest.name,
#                 max_adults=_guest.max_adults,
#                 invitations=[
#                     models.UserEventInvitation.query.filter_by(
#                         guest=_guest, event=_event
#                     )
#                     for _event in _events
#                 ],
#             )
#         )
#     return render_template(
#         "admin/admin_responses.html", events=_events, guest_list=_user_list
#     )
