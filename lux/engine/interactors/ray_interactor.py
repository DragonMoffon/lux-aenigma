from __future__ import annotations

from pyglet.math import Vec2

from lux.engine.lights.ray import LightRay

from lux.engine.colour import LuxColour
from lux.engine.interactors.interactor_edge import RayInteractorEdge


class RayInteractor:

    def __init__(self, origin: Vec2, direction: Vec2, colour: LuxColour, bounds: tuple[RayInteractorEdge]):
        self.origin = origin
        self.direction = direction
        self.colour = colour

        # The convex hull of the shape, does not necessarily represent the actual shape of the interactor
        self._bounds: tuple[RayInteractorEdge, ...] = bounds

    @property
    def bounds(self):
        return self._bounds

    def ray_hit(self, in_ray: LightRay, in_edge: RayInteractorEdge,
                left_intersection: Vec2, right_intersection: Vec2) -> tuple[LightRay, ...]:
        """
        Take in a ray, and calculate where the ray will exit

        :param in_ray: The ray which is entering the object
        :param in_edge: The edge the ray has hit
        :return: the exiting ray
        """
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}<{self.origin=}, {self.direction=}, {self.colour=}, bounds={self._bounds}>"
