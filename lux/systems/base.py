from typing import Protocol, TypeVar
from weakref import WeakSet

from lux.components.base import Component


class UpdateLoopSystem(Protocol):
    update_priority: int

    def update(self, dt: float):
        ...


class DrawLoopSystem(Protocol):
    draw_priority: int

    def draw(self):
        ...


C = TypeVar('C', bound=Component)


class _ComponentSource(Protocol):

    def get_components(self, component: type[C]) -> WeakSet[C]:
        pass


class System:
    # The list of component names that the system expects a level to have.
    # It is used to determine if a system should be used for a particular level.
    # As with everything that requires human input it is error-prone so I have an assert in place.
    requires: frozenset[type[Component]] = frozenset()
    update_priority: int = 0xffffff
    draw_priority: int = 0xffffff

    def __init__(self):
        pass

    def preload(self):
        """
        Run any thread-safe initialisation the system may need
        """
        pass

    def load(self, source: _ComponentSource):
        """
        Run any final thread-unsafe initialisation, and grab actual level components
        """
        pass

    def unload(self):
        """
        Remove any connections which may impact other levels operations.
        """
        pass