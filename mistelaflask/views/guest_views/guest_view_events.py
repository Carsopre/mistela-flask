from __future__ import annotations

from flask import Blueprint, render_template
from flask_login import current_user, login_required

from mistelaflask import models
from mistelaflask.views.guest_views.guest_view_protocol import GuestViewProtocol


class GuestViewEvents(GuestViewProtocol):
    view_name: str = "events"

    def _render_guest_view_template(self, template_name: str, **context):
        return render_template(f"guest/events/" + template_name, **context)

    @classmethod
    def register(cls, guest_blueprint: Blueprint) -> GuestViewEvents:
        _view = cls()
        guest_blueprint.add_url_rule(
            "/events/", "events_list", _view._list_view, methods=["GET"]
        )
        return _view

    @login_required
    def _list_view(self):
        _main_event = models.MainEvent.query.one()
        _dummy_main_event = models.MainEvent()
        _dummy_main_event.name = _main_event.name
        _dummy_main_event.contact = _main_event.contact
        _dummy_main_event.description = _main_event.description
        _dummy_main_event.location = _main_event.location
        _dummy_main_event.events = []
        for _invitation in models.UserEventInvitation.query.filter_by(
            guest_id=current_user.id
        ):
            _dummy_main_event.events.append(_invitation.event)

        return self._render_guest_view_template(
            "guest_event_base.html", main_event=_dummy_main_event
        )
