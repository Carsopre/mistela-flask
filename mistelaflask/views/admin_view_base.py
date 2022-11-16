from __future__ import annotations

from functools import wraps

from flask import Blueprint, current_app, request
from flask_login import config, current_user

from mistelaflask.views.admin_view_protocol import AdminViewProtocol


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in config.EXEMPT_METHODS or current_app.config.get(
            "LOGIN_DISABLED"
        ):
            pass
        elif not current_user.is_authenticated or not current_user.admin:
            return current_app.login_manager.unauthorized()

        # flask 1.x compatibility
        # current_app.ensure_sync is only available in Flask >= 2.0
        if callable(getattr(current_app, "ensure_sync", None)):
            return current_app.ensure_sync(func)(*args, **kwargs)
        return func(*args, **kwargs)

    return decorated_view


def add_url_rules(admin_blueprint: Blueprint, admin_view: AdminViewProtocol):
    admin_blueprint.add_url_rule(
        f"/{admin_view.view_name}/",
        f"{admin_view.view_name}_list",
        admin_view._list_view,
    )
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
        f"/{admin_view.view_name}/remove/<int:model_id>/",
        f"{admin_view.view_name}_remove",
        admin_view._remove_view,
    )
    admin_blueprint.add_url_rule(
        f"/{admin_view.view_name}/add/",
        f"{admin_view.view_name}_add",
        admin_view._add_view,
        methods=["GET"],
    )
    admin_blueprint.add_url_rule(
        f"/{admin_view.view_name}/add/",
        f"{admin_view.view_name}_create",
        admin_view._create_view,
        methods=["POST"],
    )
