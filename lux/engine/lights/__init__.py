from typing import NamedTuple

from pyglet.math import Vec2

from lux.engine.colour import LuxColour


class Ray(NamedTuple):
    source: Vec2
    direction: Vec2
    length: float
    colour: LuxColour
