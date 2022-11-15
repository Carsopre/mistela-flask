from __future__ import annotations

from flask import Blueprint

from mistelaflask.views.admin_view_protocol import AdminViewProtocol


def add_url_rules(admin_blueprint: Blueprint, admin_view: AdminViewProtocol):
    admin_blueprint.add_url_rule(f"/{admin_view.view_name}/", f"{admin_view.view_name}_list", admin_view._list_view)
    admin_blueprint.add_url_rule(
        f"/{admin_view.view_name}/detail/<int:model_id>/",
        f"{admin_view.view_name}_detail",
        admin_view._detail_view,
        methods=["GET"],
    )
    admin_blueprint.add_url_rule(
        f"/{admin_view.view_name}/detail/<int:model_id>/",
        f"{admin_view.view_name}_update",
        admin_view._update_view,
        methods=["POST", "PUT"],
    )
    admin_blueprint.add_url_rule(
        f"/{admin_view.view_name}/remove/<int:model_id>/", f"{admin_view.view_name}_remove", admin_view._remove_view
    )
    admin_blueprint.add_url_rule(
        f"/{admin_view.view_name}/add/", f"{admin_view.view_name}_add", admin_view._add_view, methods=["GET"]
    )
    admin_blueprint.add_url_rule(
        f"/{admin_view.view_name}/add/", f"{admin_view.view_name}_create", admin_view._create_view, methods=["POST"]
    )