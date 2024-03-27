from math import acos

from pyglet.math import Vec2

from lux.engine.lights import Ray
from lux.engine.interactors import RayInteractorEdge, RayInteractor
from lux.engine.colour import LuxColour


class PortalRayInteractor(RayInteractor):

    def __init__(self, height: float, origin: Vec2, direction: Vec2, colour: LuxColour):
        bounds = (
            RayInteractorEdge(
                Vec2(0.0, -height/2.0),
                Vec2(0.0, height/2.0),
                False
            ),
        )
        super().__init__(origin, direction, colour, bounds)
        self._sibling: PortalRayInteractor = None

    @property
    def edge(self):
        return self._bounds[0]

    def set_siblings(self, sibling):
        self._sibling, sibling._sibling = sibling, self

    def ray_hit(self, in_ray: Ray, in_edge: RayInteractorEdge, intersection_point: Vec2) -> Ray | None:
        assert in_edge is self.edge, "Portal edge not being used with portal"

        if self._sibling is None:
            return

        direction_heading = self.direction.heading

        edge_normal = in_edge.normal.rotate(direction_heading)

        edge_start = self.origin + in_edge.start.rotate(self.direction.heading)
        edge_end = self.origin + in_edge.end.rotate(self.direction.heading)

        if not in_edge.bi_dir and (in_ray.source - intersection_point).dot(edge_normal) < 0.0:
            return

        sibling = self._sibling
        sibling_edge = sibling.edge
        sibling_normal = sibling_edge.normal.rotate(sibling.direction.heading)
        sibling_start = sibling.origin + sibling_edge.start.rotate(sibling.direction.heading)
        sibling_end = sibling.origin + sibling_edge.end.rotate(sibling.direction.heading)
        sibling_diff = sibling_end - sibling_start

        portal_rotation = acos(edge_normal.dot(-sibling_normal))
        ray_direction = in_ray.direction

        edge_diff = edge_end - edge_start
        intersection_diff = intersection_point - edge_start

        fraction = 1.0 - intersection_diff.mag / edge_diff.mag

        new_source = sibling_start + sibling_diff * fraction
        new_direction = ray_direction.rotate(portal_rotation)
        new_length = in_ray.length - (intersection_point - in_ray.source).mag
        new_colour = in_ray.colour

        new_ray = Ray(new_source, new_direction, new_length, new_colour)
        return new_ray
