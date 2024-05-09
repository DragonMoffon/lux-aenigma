from __future__ import annotations
from weakref import WeakSet
from typing import Any, Protocol, Callable


class Resolvable(Protocol):
    def resolve(self, source):
        ...


class Component:
    def __init__(self, UUID: int):
        self._change_listeners: dict[str, WeakSet[Callable[[Component, str, Any], None]]] = {}
        self.UUID: int = UUID

    def serialise(self) -> dict[str, Any]:
        raise NotImplementedError()

    @classmethod
    def deserialise(cls, data: dict) -> tuple[Component, tuple[Resolvable, ...]]:
        raise NotImplementedError()

    # Change listeners for the systems that care about batching (looking at you sprite renderers)
    # They are attribute specific because idk maybe a system only cares about position?
    # This may make setting values far to slow also does it work with properties? me shall see
    def add_listener(self, attribute: str, callback: Callable):
        if attribute not in self._change_listeners:
            self._change_listeners[attribute] = WeakSet()

        self._change_listeners[attribute].add(callback)

    def remove_listener(self, attribute: str, callback: Callable):
        self._change_listeners[attribute].discard(callback)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        callbacks = self._change_listeners.get(key, ())
        for callback in callbacks:
            callback(self, key, value)