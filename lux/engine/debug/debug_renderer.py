from typing import Protocol, Any


class DebugChildRenderer(Protocol):
    child: Any

    def draw(self):
        ...


class DebugRenderer:

    def __init__(self):
        self._renderers: list[DebugChildRenderer] = []

    def draw(self):
        for renderer in self._renderers:
            renderer.draw()

    def append(self, renderer: DebugChildRenderer):
        self._renderers.append(renderer)
