from pyglet.math import Vec2

from lux.engine.interactors import RayInteractor, RayInteractorEdge
from lux.engine.lights.ray import Ray, LightRay
from lux.engine.lights.beam_light_ray import BeamLightRay
from lux.engine.colour import LuxColour


class FilterRayInteractor(RayInteractor):

    def ray_hit(self, in_ray: LightRay, in_edge: RayInteractorEdge,
                left_intersection: Vec2, right_intersection: Vec2) -> tuple[LightRay, ...]:
        new_colour = self.colour.mask(in_ray.colour)
        if new_colour == LuxColour.BLACK:
            return ()

        edge_normal = in_edge.normal

        if not in_edge.bi_dir and ((right_intersection - in_ray.origin).dot(edge_normal) >= 0.0 or (left_intersection - in_ray.origin).dot(edge_normal) >= 0.0):
            return ()

        new_left_length = in_ray.left.strength - in_ray.left.length
        new_right_length = in_ray.right.strength - in_ray.right.length

        return (BeamLightRay(new_colour,
                             Ray(left_intersection, in_ray.left.direction, new_left_length, new_left_length),
                             Ray(right_intersection, in_ray.right.direction, new_right_length, new_right_length)),)


class PolygonFilterRayInteractor(FilterRayInteractor):
    # TODO
    pass
