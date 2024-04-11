from enum import Enum

from pyglet.math import Vec2

from lux.engine.colour import LuxColour


class PlayerState(Enum):
    idle = 0
    moving = 1
    crouched = 2
    crawling = 3
    grabbing = 4


class PlayerData:
    __slots__ = (
        "colour",
        "origin",
        "direction",
        "state",
        "is_crouching",
    )

    def __init__(
            self,
            colour: LuxColour = LuxColour.WHITE,
            origin: Vec2 = Vec2(0.0, 0.0),
            direction: Vec2 = Vec2(1.0, 0.0)
    ):
        # Level Object Variables
        self.colour: LuxColour = colour
        self.origin: Vec2 = origin
        self.direction: Vec2 = direction

        # State
        self.state: PlayerState = PlayerState.idle

        # movement variables
        self.is_crouching: bool = True

        # Animation variables
