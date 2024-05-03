from typing import Protocol

from pyglet.math import Vec2
from lux.util import LuxColour


class LevelObject(Protocol):
    origin: Vec2
    direction: Vec2
    colour: LuxColour


class Controllable(Protocol):
    pass
