from __future__ import annotations

from flask import Blueprint, flash, redirect, request, url_for

from mistelaflask import db, models
from mistelaflask.utils import admin_required
from mistelaflask.views.admin_views.admin_view_base import AdminViewBase


class AdminViewEvents(AdminViewBase):
    view_name: str = "events"

    @classmethod
    def register(cls, admin_blueprint: Blueprint) -> AdminViewEvents:
        _view = cls()
        _view._add_base_url_rules(admin_blueprint, _view)
        return _view

    @admin_required
    def _list_view(self):
        _events = models.Event.query.all()
        return self._render_events_template("admin_events_list.html", events=_events)

    @admin_required
    def _detail_view(self, model_id: int):
        _event = models.Event.query.filter_by(id=model_id).first()
        return self._render_events_template(
            "admin_events_detail.html",
            event=_event,
        )

    @admin_required
    def _remove_view(self, model_id: int):
        _event: models.Event = models.Event.query.filter_by(id=model_id).first()
        _name = _event.name
        models.Event.query.filter_by(id=model_id).delete()
        db.session.commit()
        flash(f"Event {_name} has been removed.", category="danger")
        return redirect(url_for("admin.events_list"))

    @admin_required
    def _update_view(self, model_id: int):
        _event: models.Event = models.Event.query.filter_by(id=model_id).first()
        if not _event:
            flash("Event not found.", category="danger")
            return redirect(url_for("admin.events_list"))

        _event.name = request.form.get("name")
        _event.description = request.form.get("description")
        db.session.commit()
        flash(f"Event '{_event.id}' updated", category="info")
        return redirect(url_for("admin.events_list"))

    @admin_required
    def _add_view(self):
        return self._render_events_template("admin_events_add.html")

    @admin_required
    def _create_view(self):
        name = request.form.get("name")
        description = request.form.get("description")

        _event = models.Event.query.filter_by(name=name).first()
        if _event:
            flash("An event with this name already exists.", category="danger")
            return redirect(url_for("events_create"))
        _new_event = models.Event(name=name, description=description)
        db.session.add(_new_event)
        db.session.commit()
        flash(f"Added event '{name}'.", category="success")
        return redirect(url_for("admin.events_list"))
