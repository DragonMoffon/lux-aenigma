from typing import Protocol
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


class _ComponentSource(Protocol):

    def get_components(self, components: type[Component]) -> WeakSet[Component]:
        pass


class System:
    # The list of component names that the system expects a level to have.
    # It is used to determine if a system should be used for a particular level.
    # As with everything that requires human input it is error-prone so I have an assert in place.
    requires: frozenset[type[Component]] = frozenset()

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