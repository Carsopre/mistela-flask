from __future__ import annotations

from flask import Blueprint, flash, redirect, request, url_for

from mistelaflask import db, models
from mistelaflask.utils import admin_required
from mistelaflask.views.admin_views.admin_view_base import AdminViewBase


class AdminViewLocations(AdminViewBase):
    view_name: str = "locations"

    @classmethod
    def register(cls, admin_blueprint: Blueprint) -> AdminViewLocations:
        _view = cls()
        _view._add_base_url_rules(admin_blueprint)
        return _view

    @admin_required
    def _list_view(self):
        _locations = models.Location.query.all()
        return self._render_admin_view_template(
            "admin_locations_list.html", locations=_locations
        )

    @admin_required
    def _detail_view(self, model_id: int):
        _location = models.Location.query.filter_by(id=model_id).first()
        return self._render_admin_view_template(
            "admin_locations_detail.html",
            location=_location,
        )

    @admin_required
    def _remove_view(self, model_id: int):
        _location: models.Location = models.Location.query.filter_by(
            id=model_id
        ).first()
        _name = _location.name
        models.Location.query.filter_by(id=model_id).delete()
        for _main_event in models.MainEvent.query.filter_by(location_id=model_id):
            _main_event.location = None
            db.session.add(_main_event)
        db.session.commit()
        flash(
            f"Location {_name} and related invitatinos have been removed.",
            category="danger",
        )
        return redirect(url_for("admin.locations_list"))

    @admin_required
    def _update_view(self, model_id: int):
        _location: models.Location = models.Location.query.filter_by(
            id=model_id
        ).first()
        if not _location:
            flash("Location not found.", category="danger")
            return redirect(url_for("admin.locations_list"))

        _location.name = request.form.get("name", _location.name)
        _location.description = request.form.get("description", _location.description)
        _location.url_link = request.form.get("url_link", _location.url_link)
        _location.url_map = request.form.get("url_map", _location.url_map)
        db.session.commit()
        flash(f"Location '{_location.id}' updated", category="info")
        return redirect(url_for("admin.locations_list"))

    @admin_required
    def _add_view(self):
        return self._render_admin_view_template(
            "admin_locations_add.html",
            location=models.Location(),
        )

    @admin_required
    def _create_view(self):
        name = request.form.get("name")
        _location = models.Location.query.filter_by(name=name).first()
        if _location:
            flash("A location with this name already exists.", category="danger")
            return redirect(url_for("admin.locations_create"))
        _new_location = models.Location(
            name=name,
            description=request.form.get("description"),
            url_link=request.form.get("url_link"),
            url_map=request.form.get("url_map"),
        )
        db.session.add(_new_location)
        db.session.commit()
        flash(f"Added location '{name}'.", category="success")
        return redirect(url_for("admin.locations_list"))
