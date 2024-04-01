from pyglet.math import Vec2

from lux.engine.interactors.ray_interactor import RayInteractor, RayInteractorEdge
from lux.engine.lights.ray import Ray, LightRay
from lux.engine.lights.beam_light_ray import BeamLightRay
from lux.engine.colour import LuxColour


class FilterRayInteractor(RayInteractor):

    def ray_hit(self, in_ray: LightRay, in_edge: RayInteractorEdge,
                left_intersection: Vec2, right_intersection: Vec2) -> tuple[LightRay, ...]:
        direction_heading = self.direction.heading
        edge_normal = in_edge.normal.rotate(direction_heading)

        if not in_edge.bi_dir and (in_ray.right.source - right_intersection).dot(edge_normal) < 0.0 or (in_ray.left.source - left_intersection).dot(edge_normal) < 0.0:
            return ()

        new_colour = self.colour.mask(in_ray.colour)
        if new_colour == LuxColour.BLACK():
            return ()

        new_direction = in_ray.direction
        new_right_length = in_ray.left.length - (left_intersection - in_ray.left.source).mag
        new_right_strength = in_ray.left.strength - in_ray.left.length
        new_left_length = in_ray.right.length - (right_intersection - in_ray.right.source).mag
        new_left_strength = in_ray.right.strength - in_ray.right.strength

        return (BeamLightRay(new_colour,
                             Ray(right_intersection, new_direction, new_left_length, new_left_strength),
                             Ray(left_intersection, new_direction, new_right_length, new_right_strength)),)


class PolygonFilterRayInteractor(FilterRayInteractor):
    # TODO
    pass
