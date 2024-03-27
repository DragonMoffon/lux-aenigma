from typing import Protocol

from pyglet.math import Vec2

from lux.engine.colour import LuxColour


class SceneObject(Protocol):
    colour: LuxColour
    Origin: Vec2
    Direction: Vec2
