from typing import Protocol, Any

from arcade.draw_commands import draw_point

from lux.depreciated.engine.level.level_object import LevelObject

class DebugChildRenderer(Protocol):
    child: Any

    def draw(self):
        ...

    def update_child(self, new_child: Any):
        ...


class BaseChildRenderer:

    def __init__(self, child: LevelObject):
        self.child = child

    def draw(self):
        draw_point(self.child.origin.x, self.child.origin.y, self.child.colour.to_int_color(), 5.0)

    def update_child(self, new_child: LevelObject):
        self.child = new_child


class DebugRenderer:

    def __init__(self):
        self._renderers: list[DebugChildRenderer] = []

    def draw(self):
        for renderer in self._renderers:
            renderer.draw()

    def append(self, renderer: DebugChildRenderer):
        self._renderers.append(renderer)

    def remove(self, renderer: DebugChildRenderer):
        self._renderers.remove(renderer)

    def clear(self):
        self._renderers = []
