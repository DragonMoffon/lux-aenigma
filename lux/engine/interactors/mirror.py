from math import acos

from pyglet.math import Vec2

from lux.engine.lights import Ray
from lux.engine.interactors import RayInteractorEdge, RayInteractor
from lux.engine.colour import LuxColour
from lux.engine.math import Direction


class MirrorRayInteractor(RayInteractor):

    def __init__(self, height: float, origin: Vec2, direction: Vec2, colour: LuxColour):
        bounds = (
            RayInteractorEdge(
                Vec2(0.0, -height/2.0),
                Vec2(0.0, height/2.0),
                False
            ),
        )
        super().__init__(origin, direction, colour, bounds)

    @property
    def edge(self):
        return self._bounds[0]

    def ray_hit(self, in_ray: Ray, in_edge: RayInteractorEdge, intersection_point: Vec2) -> Ray | None:
        assert in_edge is self.edge, "Mirror edge not being used with mirror"

        direction_heading = self.direction.heading
        edge_normal = in_edge.normal.rotate(direction_heading)
        edge_dir = in_edge.direction.rotate(direction_heading)

        if not in_edge.bi_dir and (in_ray.source - intersection_point).dot(edge_normal) < 0.0:
            return

        parallel_component = in_ray.direction.dot(edge_normal)
        mirror_component = in_ray.direction.dot(edge_dir)

        new_direction = - edge_normal * parallel_component + edge_dir * mirror_component
        new_length = in_ray.length - (intersection_point - in_ray.source).mag
        new_colour = self.colour.mask(in_ray.colour)

        new_ray = Ray(intersection_point, new_direction, new_length, new_colour)
        return new_ray
