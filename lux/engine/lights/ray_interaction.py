import heapq

from pyglet.math import Vec2

from lux.engine.lights.ray import Ray
from lux.engine.interactors import RayInteractor, RayInteractorEdge
from lux.engine.math import get_intersection, get_segment_intersection


def calculate_ray_interaction(ray: Ray, interactors: tuple[RayInteractor, ...]) -> tuple[Vec2, RayInteractorEdge, RayInteractor] | None:
    intersecting_edges = []

    ray_start = ray.source
    ray_end = ray_start + ray.direction * ray.length
    ray_direction = ray.direction
    ray_colour = ray.colour

    for interactor in interactors:
        position = interactor.origin
        heading = interactor.direction.heading
        for edge in interactor.bounds:
            start, end, center, normal, direction = (
                position + edge.start.rotate(heading),
                position + edge.end.rotate(heading),
                position + edge.center.rotate(heading),
                edge.normal.rotate(heading),
                edge.direction.rotate(heading)
            )
            interaction_point = get_segment_intersection(ray_start, ray_end, start, end, ray_direction, direction)
            if interaction_point is None:
                continue

            diff = (interaction_point - ray_start)
            dist = diff.dot(diff)

            heapq.heappush(intersecting_edges, (dist, interaction_point, edge, interactor))

    if not intersecting_edges:
        return None

    closest_edge = heapq.heappop(intersecting_edges)

    return closest_edge[1:]


