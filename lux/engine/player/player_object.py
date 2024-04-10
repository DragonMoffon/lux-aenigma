from pyglet.math import Vec2

from lux.engine.colour import LuxColour


class PlayerData:
    __slots__ = (
        "colour",
        "origin",
        "direction"
    )

    def __init__(
            self,
            colour: LuxColour = LuxColour.WHITE,
            origin: Vec2 = Vec2(0.0, 0.0),
            direction: Vec2 = Vec2(1.0, 0.0)
    ):
        self.colour: LuxColour = colour
        self.origin: Vec2 = origin
        self.direction: Vec2 = direction
