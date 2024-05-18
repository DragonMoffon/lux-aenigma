from typing import Any, TypedDict

from pyglet.math import Vec2

from lux.util import LuxColour

from lux.components.base import Component, Resolvable


LevelObjectDict = TypedDict(
    "LevelObjectDict",
    {
        "UUID": int,
        "origin": tuple[float, float],
        "direction": tuple[float, float],
        "colour": tuple[bool, bool, bool]
    }
)


class LevelObject(Component):
    __slots__ = (
        "UUID",
        "_change_listeners"
        "origin",
        "_direction",
        "_normal",
        "colour"
    )

    def __init__(self, UUID: int, origin: Vec2, direction: Vec2, colour: LuxColour):
        super().__init__(UUID)
        self.origin: Vec2 = origin
        self._direction: Vec2 = direction
        self._normal: Vec2 = Vec2(direction.y, -direction.x)
        self.colour: LuxColour = colour

    def serialise(self) -> LevelObjectDict:
        return {
            "UUID": self.UUID,
            "origin": (self.origin.x, self.origin.y),
            "direction": (self.direction.x, self.direction.y),
            "colour": (self.colour.red, self.colour.green, self.colour.blue)
        }

    @classmethod
    def deserialise(cls, data: LevelObjectDict) -> tuple[Any, tuple[Resolvable, ...]]:
        o_x, o_y = data["origin"]
        d_x, d_y = data["direction"]
        r, g, b = data["colour"]

        return cls(data["UUID"], Vec2(o_x, o_y), Vec2(d_x, d_y), LuxColour(r, g, b)), ()

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, new_direction: Vec2):
        self._direction = new_direction
        self._normal = Vec2(new_direction.y, new_direction.x)

    @property
    def normal(self):
        return self._normal

    @normal.setter
    def normal(self, new_normal: Vec2):
        self._normal = new_normal
        self._direction = Vec2(new_normal.y, -new_normal.x)
