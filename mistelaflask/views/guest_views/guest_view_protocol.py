from __future__ import annotations

from typing import Protocol

from flask import Blueprint


class GuestViewProtocol(Protocol):
    view_name: str

    @classmethod
    def register(cls, blueprint: Blueprint) -> GuestViewProtocol:
        pass
