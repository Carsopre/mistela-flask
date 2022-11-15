from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from mistelaflask import db, models


def render_events_template(template_name: str, **context):
    return render_template("admin/events/" + template_name, **context)


class AdminEventView:
    @classmethod
    def register(cls, admin_blueprint: Blueprint) -> AdminEventView:
        _view = cls()
        admin_blueprint.add_url_rule("/events", "events_list", _view.events_list)
        admin_blueprint.add_url_rule(
            "/events/detail/<int:event_id>",
            "events_detail",
            _view.events_detail,
            methods=["GET"],
        )
        admin_blueprint.add_url_rule(
            "/events/detail/<int:event_id>",
            "events_update",
            _view.events_update,
            methods=["POST", "PUT"],
        )
        admin_blueprint.add_url_rule(
            "/events/remove/<int:event_id>", "events_remove", _view.events_remove
        )
        admin_blueprint.add_url_rule(
            "/events/add", "events_add", _view.events_add, methods=["GET"]
        )
        admin_blueprint.add_url_rule(
            "/events/add", "events_create", _view.events_create, methods=["POST"]
        )

        return _view

    @login_required
    def events_list(self):
        if not current_user.admin:
            return redirect(url_for("index"))
        _events = models.Event.query.all()
        return render_events_template("admin_events_list.html", events=_events)

    @login_required
    def events_detail(self, event_id: int):
        if not current_user.admin:
            return redirect(url_for("index"))
        _event = models.Event.query.filter_by(id=event_id).first()
        return render_events_template(
            "admin_events_detail.html",
            event=_event,
        )

    @login_required
    def events_remove(self, event_id: int):
        if not current_user.admin:
            return redirect(url_for("index"))
        _event: models.Event = models.Event.query.filter_by(id=event_id).first()
        _name = _event.name
        models.Event.query.filter_by(id=event_id).delete()
        db.session.commit()
        flash(f"Event {_name} has been removed.", category="danger")
        return redirect(url_for("admin.events_list"))

    @login_required
    def events_update(self, event_id: int):
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

    def events_add(self):
        if not current_user.admin:
            return redirect(url_for("index"))
        return render_events_template("admin_events_add.html")

    @login_required
    def events_create(self):
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
