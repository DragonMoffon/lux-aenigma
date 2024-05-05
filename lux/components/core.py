from typing import Any

from pyglet.math import Vec2
from lux.util import LuxColour

from lux.components.base import Component

class LevelObject(Component):
    __slots__ = (
        "UUID",
        "origin",
        "_direction",
        "_normal",
        "colour"
    )

    def __init__(self, UUID: int, origin: tuple[float, float], direction: tuple[float, float], colour: LuxColour):
        super().__init__(UUID)
        self.origin: Vec2 = Vec2(origin[0],origin[1])
        self._direction: Vec2 = Vec2(direction[0], direction[1])
        self._normal: Vec2 = Vec2(-direction[1], direction[0])
        self.colour: LuxColour = colour

    def serialise(self) -> dict[str, Any]:
        return {
            "UUID": self.UUID,
            "origin": (self.origin.x, self.origin.y),
            "direction": (self.direction.x, self.direction.y),
            "colour": (self.colour.red, self.colour.green, self.colour.blue)
        }

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, new_direction: Vec2):
        self._direction = new_direction
        self._normal = Vec2(-new_direction.y, new_direction.x)

    @property
    def normal(self):
        return self._normal

    @normal.setter
    def normal(self, new_normal: Vec2):
        self._normal = new_normal
        self._direction = Vec2(new_normal.y, -new_normal.x)
