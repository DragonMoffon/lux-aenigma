from pyglet.math import Vec2

from lux.engine.lights import Ray
from lux.engine.interactors import RayInteractorEdge, RayInteractor
from lux.engine.colour import LuxColour
from lux.util.maths import Direction

from lux.engine.lights.beam_light_ray import LightRay, BeamLightRay


class MirrorRayInteractor(RayInteractor):

    def __init__(self, height: float, origin: Vec2, direction: Direction, colour: LuxColour):
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

    def ray_hit(self, in_ray: LightRay, in_edge: RayInteractorEdge,
                left_intersection: Vec2, right_intersection: Vec2) -> tuple[LightRay, ...]:

        new_colour = self.colour.mask(in_ray.colour)
        if new_colour == LuxColour.BLACK():
            return ()

        edge_normal = in_edge.normal
        edge_direction = in_edge.direction

        if not in_edge.bi_dir and ((right_intersection - in_ray.origin).dot(edge_normal) >= 0.0 or (left_intersection - in_ray.origin).dot(edge_normal) >= 0.0):
            return ()

        # Since we are flipping the ray the left becomes the right and vice-versa
        new_left_length = in_ray.right.strength - in_ray.right.length
        new_right_length = in_ray.left.strength - in_ray.left.length

        left_parallel_component = in_ray.right.direction.dot(edge_normal)
        left_mirror_component = in_ray.right.direction.dot(edge_direction)

        right_parallel_component = in_ray.left.direction.dot(edge_normal)
        right_mirror_component = in_ray.left.direction.dot(edge_direction)

        new_left_direction = - edge_normal * left_parallel_component + edge_direction * left_mirror_component
        new_right_direction = - edge_normal * right_parallel_component + edge_direction * right_mirror_component

        left_ray = Ray(
            right_intersection,
            new_left_direction,
            new_left_length,
            new_left_length
        )

        right_ray = Ray(
            left_intersection,
            new_right_direction,
            new_right_length,
            new_right_length
        )

        return BeamLightRay(new_colour, left_ray, right_ray),
