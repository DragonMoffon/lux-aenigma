from __future__ import annotations
import math

from pyglet.math import Vec2

from logging import getLogger

logger = getLogger("lux")


class Direction(Vec2):
    def __init__(self, x: float = 0, y: float = 0):
        mag = (x**2.0 + y**2.0) ** 0.5
        super().__init__(x / mag, y / mag)

    @classmethod
    def degrees(cls, deg: float) -> Direction:
        rad = deg * (math.pi / 180)
        return Direction(math.cos(rad), math.sin(rad))

    @classmethod
    def NORTH(cls) -> Direction:
        return cls(0, 1)

    @classmethod
    def SOUTH(cls) -> Direction:
        return cls(0, -1)

    @classmethod
    def EAST(cls) -> Direction:
        return cls(1, 0)

    @classmethod
    def WEST(cls) -> Direction:
        return cls(-1, 0)

    @classmethod
    def NORTHEAST(cls) -> Direction:
        return cls(1, 1)

    @classmethod
    def SOUTHEAST(cls) -> Direction:
        return cls(1, -1)

    @classmethod
    def NORTHWEST(cls) -> Direction:
        return cls(1, -1)

    @classmethod
    def SOUTHWEST(cls) -> Direction:
        return cls(-1, -1)


def cross_2d(a: Vec2, b: Vec2):
    return (a.x * b.y) - (a.y * b.x)


def get_segment_intersection(p: Vec2, p_e: Vec2, q: Vec2, q_e: Vec2) -> Vec2 | None:
    # https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect

    # Find the diff from start to end of each segment
    r = (p_e - p)
    s = (q_e - q)

    # Find the angle between the two diffs if they are parallel then we don't consider it an interaction
    direction_interaction = cross_2d(r, s)

    if direction_interaction == 0.0:
        logger.debug(f"segment<{p} - {p_e}> is parallel to segment<{q} - {q_e}>")
        return None

    # Find how the ratio of how far along each segment the interaction is
    t_ratio = cross_2d((q - p), s)
    u_ratio = cross_2d((q - p), r)

    # Calculate the actual fraction distance along
    t = t_ratio / direction_interaction
    u = u_ratio / direction_interaction

    logger.debug(f"t: {t}, u: {u}")

    # If t and u aren't between 0 and 1 then the intersection is outside the segments
    if not (0.0 <= u <= 1.0 and 0.0 <= t <= 1.0):
        logger.debug(f"segment<{p} - {p_e}> misses segment<{q} - {q_e}>")
        return None

    logger.debug(f"segment<{p} - {p_e}> intersects segment<{q} - {q_e}> at {p + r * t}")
    return p + r * t


def get_intersection(o1: Vec2, d1: Vec2, o2: Vec2, d2: Vec2) -> Vec2 | None:
    # Same logic as get segment intersection we just don't care if t and u go past 1.0

    direction_interaction = cross_2d(d1, d2)

    # Two lines are parallel
    if direction_interaction == 0.0:
        logger.debug(f"line<{o1} + t*{d1}> is parallel to line<{o2} + u*{d2}>")
        return None

    # find of far along line one line two intersects
    # because we don't care about if the segments interact we just need to find t
    t = cross_2d(o2 - o1, d2) / direction_interaction

    logger.debug(f"line<{o1} + t*{d1}> intersects line<{o2} + u*{d2}> at {o1 + d1 * t}")
    return o1 + d1 * t
