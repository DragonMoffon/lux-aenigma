from typing import Protocol, runtime_checkable

from pyglet.math import Vec2

from lux.engine.colour import LuxColour


@runtime_checkable
class LevelObject(Protocol):
    colour: LuxColour
    origin: Vec2
    direction: Vec2
