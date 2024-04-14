from math import degrees, radians

from pyglet.math import Vec2

from lux.engine.level.level_object import LevelObject


class DegreeOfFreedom:
    """
    A base class which defines how the player may control a subject LevelObject.

    Will be used by puzzles to move objects like projectors and mirrors around.
    """
    pass


class RotationDOF(DegreeOfFreedom):
    pass


class AxisDOF(DegreeOfFreedom):
    pass


class ToggleDOF(DegreeOfFreedom):
    pass
