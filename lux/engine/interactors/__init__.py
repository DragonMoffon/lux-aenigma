from pyglet.math import Vec2

from lux.engine.lights import Ray
from lux.engine.color import LuxColour


class RayInteractorEdge:
    __slots__ = (
        "_start",
        "_end",
        "_normal",
        "_bi_dir"
    )

    def __init__(self, start: Vec2, end: Vec2, bi_dir: bool):
        self._start: Vec2 = start
        self._end: Vec2 = end

        direction = (end - start).normalize()
        self._normal: Vec2 = Vec2(direction.y, -direction.x)
        self._bi_dir: bool = bi_dir

    @property
    def center(self):
        return (self._start + self._end) / 2.0


class RayInteractor:

    def __init__(self, origin: Vec2, direction: Vec2, colour: LuxColour, bounds: tuple[RayInteractorEdge]):
        self.origin = origin
        self.direction = direction
        self.colour = colour

        # The convex hull of the shape, does not necessarily represent the actual shape of the interactor
        self._bounds: tuple[RayInteractorEdge, ...] = bounds

    @property
    def bound(self):
        return self._bounds

    def ray_hit(self, in_ray: Ray, in_edge: RayInteractorEdge, intersection_point: Vec2) -> Ray:
        """
        Take in a ray, and calculate where the ray will exit

        :param in_ray: The ray which is entering the object
        :param in_edge: The edge the ray has hit
        :return: the exiting ray
        """
        raise NotImplementedError()
