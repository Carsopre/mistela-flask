from __future__ import annotations

from flask import Blueprint, render_template
from flask_login import login_required

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
        _events = models.Event.query.all()
        _main_event = models.MainEvent.query.one()
        return self._render_guest_view_template(
            "guest_event_base.html", events=_events, main_event=_main_event
        )
