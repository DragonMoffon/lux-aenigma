from pyglet.math import Vec2

from lux.engine.colour import LuxColour
from lux.engine.level.level_object import LevelObject
from lux.engine.control_points.dof import DegreeOfFreedom


class ControlPoint:

    def __init__(self, subject: LevelObject, relative_pos: Vec2, colour: LuxColour, dof: tuple[DegreeOfFreedom] = None):
        self.subject: LevelObject = subject
        self.colour: LuxColour = colour
        self._relative_pos: Vec2 = relative_pos
        self.degrees_of_freedom: tuple[DegreeOfFreedom] = dof or tuple()

    def get_grab_distance(self, lux_pos: Vec2, lux_colour: LuxColour):
        if lux_colour.mask(self.colour) == LuxColour.BLACK:
            return float('inf')

        abs_pos = self.absolute_position
        diff = lux_pos - abs_pos
        return diff.dot(diff)

    @property
    def absolute_position(self):
        f = self.subject.direction
        r = Vec2(-f.y, f.x)
        return self.subject.origin + f * self._relative_pos.x + r * self._relative_pos.y

    @property
    def relative_position(self):
        f = self.subject.direction
        r = Vec2(-f.y, f.x)
        return f * self._relative_pos.x + r * self._relative_pos.y

    def pull(self, lux_pos: Vec2, force: float):
        abs_pos = self.absolute_position
        force_direction = lux_pos - abs_pos
        for dof in self.degrees_of_freedom:
            dof.pull(force_direction, self.relative_position, force)
