from __future__ import annotations
from logging import getLogger
import math

from pyglet.math import Vec2

from lux.util.classproperty import classproperty

logger = getLogger("lux")


class Direction(Vec2):
    def __init__(self, x: float = 0, y: float = 0):
        mag = (x**2.0 + y**2.0) ** 0.5
        super().__init__(x / mag, y / mag)

    @property
    def degrees(self) -> float:
        return (self.heading / (math.pi / 180)) % 360

    @property
    def name(self) -> str:
        closest_dir = ""
        if 0 <= self.degrees < 22.5 or 337.5 <= self.degrees < 360:
            closest_dir = "NORTH"
        elif 22.5 <= self.degrees < 67.5:
            closest_dir = "NORTHEAST"
        elif 67.5 <= self.degrees < 112.5:
            closest_dir = "EAST"
        elif 112.5 <= self.degrees < 157.5:
            closest_dir = "SOUTHEAST"
        elif 157.5 <= self.degrees < 202.5:
            closest_dir = "SOUTH"
        elif 202.5 <= self.degrees < 247.5:
            closest_dir = "SOUTHWEST"
        elif 247.5 <= self.degrees < 292.5:
            closest_dir = "WEST"
        elif 292.5 <= self.degrees < 337.5:
            closest_dir = "NORTHWEST"
        if self.degrees not in [0.0, 45.0, 90.0, 135.0, 180.0, 225.0, 270.0, 315.0, 360.0]:
            closest_dir = "~" + closest_dir
        return closest_dir

    @classmethod
    def from_degrees(cls, deg: float) -> Direction:
        rad = deg * (math.pi / 180)
        return Direction(math.cos(rad), math.sin(rad))

    def to_normal(self) -> Direction:
        return Direction(-self.y, self.x)

    @classproperty
    def NORTH(cls) -> Direction:
        return cls(0, 1)

    @classproperty
    def SOUTH(cls) -> Direction:
        return cls(0, -1)

    @classproperty
    def EAST(cls) -> Direction:
        return cls(1, 0)

    @classproperty
    def WEST(cls) -> Direction:
        return cls(-1, 0)

    @classproperty
    def NORTHEAST(cls) -> Direction:
        return cls(1, 1)

    @classproperty
    def SOUTHEAST(cls) -> Direction:
        return cls(1, -1)

    @classproperty
    def NORTHWEST(cls) -> Direction:
        return cls(-1, 1)

    @classproperty
    def SOUTHWEST(cls) -> Direction:
        return cls(-1, -1)

    def __str__(self) -> str:
        out_name = self.name if "~" not in self.name else f"{self.name} ({round(self.degrees, 3)}deg)"
        return f"Direction({out_name})"

    def __repr__(self) -> str:
        return self.__str__()


def cross_2d(a: Vec2, b: Vec2):
    return (a.x * b.y) - (a.y * b.x)


def get_segment_intersection(p: Vec2, p_e: Vec2, q: Vec2, q_e: Vec2) -> Vec2 | None:
    # https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect

    # Find the diff from start to end of the first segment
    r = (p_e - p)

    t = get_segment_intersection_fraction(p, p_e, q, q_e)
    if t is None:
        return None

    # Use the fraction along with p and r to find the intersection point
    return p + r * t


def get_segment_intersection_fraction(p: Vec2, p_e: Vec2, q: Vec2, q_e: Vec2) -> float | None:
    # https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
    # Same logic as segment intersection, but we don't do the final conversion to a Vec2.

    # Find the diff from start to end of each segment
    r = (p_e - p)
    s = (q_e - q)

    # Find the angle between the two diffs if they are parallel then we don't consider it an interaction
    direction_interaction = cross_2d(r, s)

    if direction_interaction == 0.0:
        # logger.debug(f"segment<{p} - {p_e}> is parallel to segment<{q} - {q_e}>")
        return None

    # Find how the ratio of how far along each segment the interaction is
    t_ratio = cross_2d((q - p), s)
    u_ratio = cross_2d((q - p), r)

    # Calculate the actual fraction distance along
    t = t_ratio / direction_interaction
    u = u_ratio / direction_interaction

    # If t and u aren't between 0 and 1 then the intersection is outside the segments
    if not (0.0 <= u <= 1.0 and 0.0 <= t <= 1.0):
        # logger.debug(f"segment<{p} - {p_e}> misses segment<{q} - {q_e}>")
        return None

    # logger.debug(f"segment<{p} - {p_e}> intersects segment<{q} - {q_e}> at {p + r * t}")
    return t


def get_intersection(o1: Vec2, d1: Vec2, o2: Vec2, d2: Vec2) -> Vec2 | None:
    # https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
    t = get_intersection_fraction(o1, d1, o2, d2)
    if t is None:
        return None

    return o1 + d1 * t


def get_intersection_fraction(o1: Vec2, d1: Vec2, o2: Vec2, d2: Vec2) -> float | None:
    # https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
    # Same logic as the segment intersection but we don't care if t or u are outside the 0-1 range.

    direction_interaction = cross_2d(d1, d2)

    # Two lines are parallel
    if direction_interaction == 0.0:
        return None

    # find how far along line one line two intersects
    # because we don't care about if the segments interact we just need to find t
    t = cross_2d(o2 - o1, d2) / direction_interaction

    return t
