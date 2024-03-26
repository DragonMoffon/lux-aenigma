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
        sibling = self._sibling
        sibling_edge = sibling.edge

        ray_direction = in_ray.direction
        sibling_normal = self._sibling.direction

        if not in_edge.bi_dir and ray_direction.dot(sibling_normal) > 0.0:
            return None

        edge_dir = in_edge.end - in_edge.start

        intersection_dir = intersection_point - in_edge.start
        intersection_fraction = edge_dir.dot(intersection_dir) / edge_dir.mag

        new_source = sibling_edge.start + intersection_fraction * (sibling_edge.end - sibling_edge.start)

