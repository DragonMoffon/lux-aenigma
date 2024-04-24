from math import degrees, radians

from pyglet.math import Vec2

from lux.engine.level.level_object import LevelObject


class DegreeOfFreedom:
    """
    A base class which defines how the player may control a subject LevelObject.

    Will be used by puzzles to move objects like projectors and mirrors around.
    """
    def __init__(self, target: LevelObject):
        self._target: LevelObject = target

    def pull(self, force_direction: Vec2, relative_axis: Vec2, force: float, ):
        raise NotImplementedError()


class RotationDOF(DegreeOfFreedom):

    def __init__(self, target: LevelObject, min_angle: float = -180.0, max_angle: float = 180.0, is_repeating: bool = True):
        super().__init__(target)
        self._is_repeating: bool = is_repeating
        self._min_angle: float = min_angle
        self._max_angle: float = max_angle

        self._base_axis = target.direction
        self._base_heading = target.direction.heading

    def _get_heading_diff(self, a: Vec2, b: Vec2):
        pass

    def pull(self, force_direction: Vec2, relative_axis: Vec2, force: float):
        # This pull method isn't pretty or fast, but it should be only one of a handful of DoF being
        # used at once.

        f_dir = force_direction.normalize()
        r_dir = relative_axis.normalize()
        r_dir = Vec2(-r_dir.y, r_dir.x)

        angle_change = force * r_dir.dot(f_dir)
        new_direction = self._target.direction.rotate(radians(angle_change))

        self._target.direction = new_direction

        # # Get the difference in heading should be between -180 and 180 degrees.
        # heading_diff = degrees(new_direction.heading - self._base_heading) % 180

        # # If the dof does not repeat then we clamp the rotation
        # if not self._is_repeating:
        #     new_heading = radians(min(self._max_angle, max(self._min_angle, heading_diff))) + self._base_heading
        #     self._target.direction = Vec2.from_polar(1.0, new_heading)
        #     return

        # If the Dof does repeat then we want to cycle back around to the max.


class AxisDOF(DegreeOfFreedom):
    pass


class ToggleDOF(DegreeOfFreedom):
    pass
