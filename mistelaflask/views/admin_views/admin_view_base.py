from __future__ import annotations

from abc import abstractclassmethod, abstractmethod

from flask import Blueprint, Response, render_template

from mistelaflask.utils import admin_required
from mistelaflask.views.admin_views.admin_view_protocol import AdminViewProtocol


class AdminViewBase(AdminViewProtocol):
    def _render_events_template(self, template_name: str, **context):
        return render_template(f"admin/{self.view_name}/" + template_name, **context)

    def _add_base_url_rules(self, admin_blueprint: Blueprint):
        admin_blueprint.add_url_rule(
            f"/{self.view_name}/",
            f"{self.view_name}_list",
            self._list_view,
        )
        admin_blueprint.add_url_rule(
            f"/{self.view_name}/detail/<int:model_id>/",
            f"{self.view_name}_detail",
            self._detail_view,
            methods=["GET"],
        )
        admin_blueprint.add_url_rule(
            f"/{self.view_name}/detail/<int:model_id>/",
            f"{self.view_name}_update",
            self._update_view,
            methods=["POST", "PUT"],
        )
        admin_blueprint.add_url_rule(
            f"/{self.view_name}/remove/<int:model_id>/",
            f"{self.view_name}_remove",
            self._remove_view,
        )
        admin_blueprint.add_url_rule(
            f"/{self.view_name}/add/",
            f"{self.view_name}_add",
            self._add_view,
            methods=["GET"],
        )
        admin_blueprint.add_url_rule(
            f"/{self.view_name}/add/",
            f"{self.view_name}_create",
            self._create_view,
            methods=["POST"],
        )

    @classmethod
    @abstractclassmethod
    def register(cls, blueprint: Blueprint) -> AdminViewProtocol:
        pass

    @admin_required
    @abstractmethod
    def _list_view(self) -> Response:
        pass

    @admin_required
    @abstractmethod
    def _detail_view(self, model_id: int) -> Response:
        pass

    @admin_required
    @abstractmethod
    def _remove_view(self, model_id: int) -> Response:
        pass

    @admin_required
    @abstractmethod
    def _update_view(self, model_id: int) -> Response:
        pass

    @admin_required
    @abstractmethod
    def _add_view(self) -> Response:
        pass

    @admin_required
    @abstractmethod
    def _create_view(self) -> Response:
        pass
