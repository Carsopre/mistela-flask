from __future__ import annotations

from typing import Protocol

from flask import Blueprint, Response
from flask_login import login_required


class AdminViewProtocol(Protocol):
    @classmethod
    def register(cls, blueprint: Blueprint) -> AdminViewProtocol:
        pass

    @login_required
    def _list_view(self) -> Response:
        pass

    @login_required
    def _detail_view(self, model_id: int) -> Response:
        pass

    @login_required
    def _remove_view(self, model_id: int) -> Response:
        pass

    @login_required
    def _update_view(self, model_id: int) -> Response:
        pass

    @login_required
    def _add_view(self) -> Response:
        pass

    @login_required
    def _create_view(self) -> Response:
        pass
