from __future__ import annotations

from flask import Blueprint, flash, redirect, request, url_for

from mistelaflask import db, models
from mistelaflask.utils import admin_required
from mistelaflask.views.admin_views.admin_view_base import AdminViewBase


class AdminViewMainEvents(AdminViewBase):
    view_name: str = "main_events"

    @classmethod
    def register(cls, admin_blueprint: Blueprint) -> AdminViewMainEvents:
        _view = cls()
        _view._add_base_url_rules(admin_blueprint)
        return _view

    @admin_required
    def _list_view(self):
        _events = models.MainEvent.query.all()
        return self._render_admin_view_template(
            "admin_main_events_list.html", main_events=_events
        )

    @admin_required
    def _detail_view(self, model_id: int):
        _event = models.MainEvent.query.filter_by(id=model_id).first()
        return self._render_admin_view_template(
            "admin_main_events_detail.html",
            main_event=_event,
            locations=models.Location.query.all(),
        )

    @admin_required
    def _remove_view(self, model_id: int):
        _event: models.MainEvent = models.MainEvent.query.filter_by(id=model_id).first()
        _name = _event.name
        models.Event.query.filter_by(main_event_id=model_id).delete()
        db.session.commit()
        flash(
            f"Main event {_name} and related events have been removed.",
            category="danger",
        )
        return redirect(url_for("admin.main_events_list"))

    @admin_required
    def _update_view(self, model_id: int):
        _event: models.MainEvent = models.MainEvent.query.filter_by(id=model_id).first()
        if not _event:
            flash("Main event not found.", category="danger")
            return redirect(url_for("admin.main_events_list"))

        # _event.main_event_id = int(request.form.get("select_main_event"))
        _event.name = request.form.get("name", _event.name)
        _event.description = request.form.get("description", _event.description)
        _event.contact = request.form.get("contact", _event.description)
        _location = request.form.get("location", None)
        _event.location_id = int(_location) if _location else _event.location_id
        db.session.commit()
        flash(f"Event '{_event.id}' updated", category="info")
        return redirect(url_for("admin.main_events_list"))

    @admin_required
    def _add_view(self):
        return self._render_admin_view_template(
            "admin_main_events_add.html",
            main_event=models.MainEvent(),
            locations=models.Location.query.all(),
        )

    @admin_required
    def _create_view(self):

        name = request.form.get("name")
        _location = request.form.get("location", None)
        _event = models.MainEvent.query.filter_by(name=name).first()
        if _event:
            flash("A main event with this name already exists.", category="danger")
            return redirect(url_for("admin.main_events_create"))
        _new_event = models.MainEvent(
            name=name,
            description=request.form.get("description"),
            contact=request.form.get("contact"),
            location_id=int(_location) if _location else None,
        )
        db.session.add(_new_event)
        db.session.commit()
        flash(f"Added event '{name}'.", category="success")
        return redirect(url_for("admin.main_events_list"))
