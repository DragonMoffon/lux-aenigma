from __future__ import annotations

from typing import Any, Protocol


class Resolvable(Protocol):
    def resolve(self, source):
        ...


class Component:
    def __init__(self, UUID: int):
        self.UUID: int = UUID

    def serialise(self) -> dict[str, Any]:
        raise NotImplementedError()

    @classmethod
    def deserialise(cls, data: dict) -> tuple[Any, tuple[Resolvable, ...]]:
        raise NotImplementedError()
