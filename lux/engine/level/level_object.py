from typing import Protocol

from pyglet.math import Vec2

from lux.engine.colour import LuxColour
from lux.util.maths import Direction


class LevelObject(Protocol):
    colour: LuxColour
    origin: Vec2
    direction: Direction
