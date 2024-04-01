from pyglet.math import Vec2

from lux.engine.interactors.ray_interactor import RayInteractor, RayInteractorEdge
from lux.engine.lights import Ray
from lux.engine.colour import LuxColour


class FilterRayInteractor(RayInteractor):

    def ray_hit(self, in_ray: Ray, in_edge: RayInteractorEdge, intersection_point: Vec2) -> Ray | None:
        assert in_edge in self._bounds, "Edge is not part of Filter"

        direction_heading = self.direction.heading
        edge_normal = in_edge.normal.rotate(direction_heading)

        if not in_edge.bi_dir and (in_ray.source - intersection_point).dot(edge_normal) < 0.0:
            return None

        new_colour = self.colour.mask(in_ray.colour)
        if new_colour == LuxColour.BLACK():
            return None

        print(new_colour)

        new_source = intersection_point
        new_direction = in_ray.direction
        new_length = in_ray.length - (intersection_point - in_ray.source).mag

        return Ray(new_source, new_direction, new_length, new_colour)


class PolygonFilterRayInteractor(FilterRayInteractor):
    # TODO
    pass
