from __future__ import annotations

from typing import Protocol

from flask import Blueprint, Response

from mistelaflask.utils import admin_required


class AdminViewProtocol(Protocol):
    view_name: str

    @classmethod
    def register(cls, blueprint: Blueprint) -> AdminViewProtocol:
        pass

    @admin_required
    def _list_view(self) -> Response:
        pass

    @admin_required
    def _detail_view(self, model_id: int) -> Response:
        pass

    @admin_required
    def _remove_view(self, model_id: int) -> Response:
        pass

    @admin_required
    def _update_view(self, model_id: int) -> Response:
        pass

    @admin_required
    def _add_view(self) -> Response:
        pass

    @admin_required
    def _create_view(self) -> Response:
        pass
