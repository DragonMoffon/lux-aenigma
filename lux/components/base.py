from __future__ import annotations
from weakref import WeakSet
from typing import Any, Protocol, Callable


class Resolvable(Protocol):
    def resolve(self, source):
        ...


class Component:
    def __init__(self, UUID: int):
        self._change_listeners: dict[str, set[Callable[[Component, str, Any], None]]] = {} # MAKE SURE THIS ISN'T LEAKING MEMORY ANYWHERE!!!!
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
            self._change_listeners[attribute] = set()

        self._change_listeners[attribute].add(callback)

    def add_listeners(self, attributes: tuple[str, ...], callback: Callable):
        for attribute in attributes:
            self.add_listener(attribute, callback)

    def remove_listener(self, attribute: str, callback: Callable):
        self._change_listeners[attribute].discard(callback)

    def remove_listeners(self, attributes: tuple[str, ...], callback: Callable):
        for attribute in attributes:
            self.remove_listener(attribute, callback)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        callbacks = self._change_listeners.get(key, ())
        for callback in callbacks:
            callback(self, key, value)
