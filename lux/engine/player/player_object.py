from enum import Enum

from pyglet.math import Vec2

from lux.util.colour import LuxColour
from lux.engine.control_points.control_point import ControlPoint


class PlayerState(Enum):
    IDLE = 0
    MOVING = 1
    CROUCHED = 2
    CRAWLING = 3
    GRABBING = 4
    PULLING = 5


class PlayerConsts:
    GRAB_RADIUS: float = 20.0**2.0


class PlayerData:
    __slots__ = (
        "colour",
        "origin",
        "direction",
        "state",
        "velocity",
        "is_crouching",
        "is_grabbing",
        "grabbed_control_point"
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
        self.state: PlayerState = PlayerState.IDLE

        # movement variables
        self.velocity: Vec2 = Vec2()
        self.is_crouching: bool = False

        # Control point Variable
        self.is_grabbing: bool = False
        self.grabbed_control_point: ControlPoint | None = None
