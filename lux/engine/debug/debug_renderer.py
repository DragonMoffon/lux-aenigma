from typing import Protocol, Any


class DebugChildRenderer(Protocol):
    child: Any

    def draw(self):
        ...

    def update_child(self, new_child: Any):
        ...


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
