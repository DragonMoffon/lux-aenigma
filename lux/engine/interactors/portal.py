from __future__ import annotations

from pyglet.math import Vec2

from lux.engine.lights import Ray
from lux.engine.interactors import RayInteractorEdge, RayInteractor
from lux.engine.colour import LuxColour

from lux.engine.lights.beam_light_ray import LightRay, BeamLightRay


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
        self._sibling_ratio: float = 0.0

    @property
    def edge(self):
        return self._bounds[0]

    def set_siblings(self, sibling):
        self._sibling, sibling._sibling = sibling, self
        self._sibling_ratio = self._sibling.edge.diff.mag / self.edge.diff.mag
        sibling._sibling_ratio = self.edge.diff.mag / self._sibling.edge.diff.mag
        print(self._sibling_ratio)

    @classmethod
    def create_pair(cls, height: float, colour: LuxColour, origin_a: Vec2, direction_a: Vec2, origin_b: Vec2, direction_b: Vec2) -> tuple[PortalRayInteractor]:
        portal_a = cls(height, origin_a, direction_a, colour)
        portal_b = cls(height, origin_b, direction_b, colour)
        portal_a.set_siblings(portal_b)
        return (portal_a, portal_b)

    def ray_hit(self, in_ray: LightRay, in_edge: RayInteractorEdge,
                left_intersection: Vec2, right_intersection: Vec2) -> tuple[LightRay, ...]:
        if self._sibling is None:
            return ()

        new_colour = self.colour.mask(in_ray.colour)
        if new_colour == LuxColour.BLACK:
            return ()

        edge_normal = in_edge.normal
        edge_direction = in_edge.direction

        if not in_edge.bi_dir and ((right_intersection - in_ray.origin).dot(edge_normal) >= 0.0 or (left_intersection - in_ray.origin).dot(edge_normal) >= 0.0):
            return ()

        edge_start = self.origin + self.edge.start.rotate(self.direction.heading)
        edge_end = self.origin + self.edge.end.rotate(self.direction.heading)
        edge_diff = (edge_end - edge_start)
        edge_len_sqr = edge_diff.dot(edge_diff)

        new_left_length = in_ray.left.strength - in_ray.left.length
        new_right_length = in_ray.right.strength - in_ray.right.length

        sibling = self._sibling
        sibling_edge = sibling.edge
        sibling_origin = sibling.origin
        sibling_heading = sibling.direction.heading

        sibling_normal = sibling_edge.normal.rotate(sibling_heading)
        sibling_direction = sibling_edge.direction.rotate(sibling_heading)

        sibling_start = sibling_origin + sibling_edge.start.rotate(sibling_heading)
        sibling_end = sibling_origin + sibling_edge.end.rotate(sibling_heading)
        sibling_diff = sibling_end - sibling_start

        # Figure the output edge direction. We mirror it in the normal direction because we want it to come
        # out of the portal edge rather than go into it.
        left_parallel_component = in_ray.left.direction.dot(edge_normal)
        left_mirror_component = in_ray.left.direction.dot(edge_direction)
        new_left_direction = - sibling_normal * left_parallel_component - sibling_direction * left_mirror_component

        right_parallel_component = in_ray.right.direction.dot(edge_normal)
        right_mirror_component = in_ray.right.direction.dot(edge_direction)
        new_right_direction = - sibling_normal * right_parallel_component - sibling_direction * right_mirror_component

        new_left_source = sibling_end + (left_intersection - edge_start) * self._sibling_ratio
        new_right_source = sibling_end + (right_intersection - edge_start) * self._sibling_ratio

        left_ray = Ray(
            new_left_source,
            new_left_direction,
            new_left_length,
            new_left_length
        )

        right_ray = Ray(
            new_right_source,
            new_right_direction,
            new_right_length,
            new_right_length
        )

        return BeamLightRay(new_colour, left_ray, right_ray),
