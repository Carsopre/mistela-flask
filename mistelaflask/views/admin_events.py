from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from mistelaflask import db, models
from mistelaflask.views.admin_view_protocol import AdminViewProtocol


class AdminEventView(AdminViewProtocol):
    def _render_events_template(self, template_name: str, **context):
        return render_template("admin/events/" + template_name, **context)

    @classmethod
    def register(cls, admin_blueprint: Blueprint) -> AdminEventView:
        _view = cls()
        admin_blueprint.add_url_rule("/events", "events_list", _view._list_view)
        admin_blueprint.add_url_rule(
            "/events/detail/<int:event_id>",
            "events_detail",
            _view._detail_view,
            methods=["GET"],
        )
        admin_blueprint.add_url_rule(
            "/events/detail/<int:event_id>",
            "events_update",
            _view._update_view,
            methods=["POST", "PUT"],
        )
        admin_blueprint.add_url_rule(
            "/events/remove/<int:event_id>", "events_remove", _view._remove_view
        )
        admin_blueprint.add_url_rule(
            "/events/add", "events_add", _view._add_view, methods=["GET"]
        )
        admin_blueprint.add_url_rule(
            "/events/add", "events_create", _view._create_view, methods=["POST"]
        )

        return _view

    @login_required
    def _list_view(self):
        if not current_user.admin:
            return redirect(url_for("index"))
        _events = models.Event.query.all()
        return self._render_events_template("admin_events_list.html", events=_events)

    @login_required
    def _detail_view(self, event_id: int):
        if not current_user.admin:
            return redirect(url_for("index"))
        _event = models.Event.query.filter_by(id=event_id).first()
        return self._render_events_template(
            "admin_events_detail.html",
            event=_event,
        )

    @login_required
    def _remove_view(self, event_id: int):
        if not current_user.admin:
            return redirect(url_for("index"))
        _event: models.Event = models.Event.query.filter_by(id=event_id).first()
        _name = _event.name
        models.Event.query.filter_by(id=event_id).delete()
        db.session.commit()
        flash(f"Event {_name} has been removed.", category="danger")
        return redirect(url_for("admin.events_list"))

    @login_required
    def _update_view(self, event_id: int):
        if not current_user.admin:
            return redirect(url_for("index"))
        _event: models.Event = models.Event.query.filter_by(id=event_id).first()
        if not _event:
            flash("Event not found.", category="danger")
            return redirect(url_for("admin.events_list"))

        _event.name = request.form.get("name")
        _event.description = request.form.get("description")
        db.session.commit()
        flash(f"Event '{_event.id}' updated", category="info")
        return redirect(url_for("admin.events_list"))

    @login_required
    def _add_view(self):
        if not current_user.admin:
            return redirect(url_for("index"))
        return self._render_events_template("admin_events_add.html")

    @login_required
    def _create_view(self):
        if not current_user.admin:
            return redirect(url_for("index"))
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
