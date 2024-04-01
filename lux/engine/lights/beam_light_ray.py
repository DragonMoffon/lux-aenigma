from __future__ import annotations
from typing import TYPE_CHECKING, Generator

from pyglet.math import Vec2

from lux.engine.lights.ray import Ray, LightRay
from lux.engine.colour import LuxColour
from lux.util.maths import get_intersection, get_segment_intersection, get_intersection_fraction
from lux.engine.interactors.interactor_edge import RayInteractorEdge

if TYPE_CHECKING:
    from lux.engine.interactors.ray_interactor import RayInteractor


class BeamLightRay(LightRay):
    """
    When a light ray is completely parallel it makes finding the intersections much easier
    """

    def __init__(self, colour: LuxColour, left: Ray, right: Ray):
        if left.direction != right.direction:
            raise ValueError("The left and right edges of a Beam should be parallel")

        origin = (left.source + right.source) / 2.0
        normal = (left.source - right.source).normalize()
        direction = Vec2(normal.y, -normal.x)

        super().__init__(origin, direction, colour, left, right)
        self.normal = normal

    def __str__(self):
        return f"BeamLightRay<{self.origin=}, {self.left=}, {self.right=}>"

    def _kill(self):
        self.left = None
        self.right = None

    def _generate_points(self, edges) -> Generator[tuple[Vec2, Vec2, RayInteractorEdge]]:
        left_source = self.left.source
        right_source = self.right.source
        beam_dir = self.left.direction
        beam_normal = Vec2(self.left.direction.y, -self.left.direction.x)
        base_normal = self.normal

        right_sink = right_source + beam_dir * self.right.length
        left_sink = left_source + beam_dir * self.left.length

        for edge in edges:
            start_point = edge.start
            end_point = edge.end

            if (start_point - left_source).dot(beam_dir) < 0.0 and (end_point - left_source).dot(beam_dir) < 0.0:
                print("Behind Beam")
                continue

            if (start_point - left_sink).dot(beam_dir) > 0.0 and (end_point - left_sink).dot(beam_dir) < 0.0:
                print("Ahead Beam")
                continue

            in_beam = False

            if ((start_point - left_source).dot(beam_normal) > 0.0) == ((start_point - right_source).dot(beam_normal) < 0.0):
                print("Start in beam")
                in_beam = True

            if ((end_point - left_source).dot(beam_normal) > 0.0) == ((end_point - right_source).dot(beam_normal) < 0.0):
                print("End in beam")
                in_beam = True

            if ((start_point - left_source).dot(beam_normal) > 0.0) == ((end_point - left_source).dot(beam_normal) < 0.0):
                print("Edge crossed beam")
                in_beam = True

            if not in_beam:
                continue

            start_intersection = get_intersection(left_source, self.normal, start_point, beam_dir)
            if start_intersection is not None:
                yield start_point, start_intersection, edge

            end_intersection = get_intersection(left_source, self.normal, end_point, beam_dir)
            if end_intersection is not None:
                yield end_point, end_intersection, edge

        # Add the very end of the beam to the calculations. even though they would normally fail the filtering
        end_edge = RayInteractorEdge(right_sink, left_sink, True)
        yield right_sink, right_source, end_edge
        yield left_sink, left_source, end_edge

    def _propagate(self, edge_to_interactor_map: dict[RayInteractorEdge, RayInteractor]) -> tuple[tuple[LightRay, RayInteractorEdge, Vec2, Vec2], ...]:
        if self.left is None or self.right is None:
            raise ValueError("This Light Beam has been killed how are you propagating it?")

        # Pull out values, so we don't use the dot notation so much
        right_source = self.right.source
        left_source = self.left.source
        beam_dir = self.right.direction
        beam_normal = self.normal
        end_normal = (self.left.source - self.right.source).normalize()

        right_sink = right_source + beam_dir * self.right.length
        left_sink = left_source + beam_dir * self.left.length

        points_sorted = sorted(
            self._generate_points(edge_to_interactor_map.keys()),
            key=lambda p: (p[0] - right_source).dot(beam_normal)
        )

        finalised_beams: list[tuple[LightRay, RayInteractorEdge, Vec2, Vec2]] = list()
        
        end_fraction = get_intersection_fraction(
            right_sink, end_normal,
            points_sorted[0][1], beam_dir
        )
        
        right_ray: Ray = Ray(
            points_sorted[0][1],
            beam_dir,
            (points_sorted[0][0] - points_sorted[0][1]).mag,
            self.right.strength + end_fraction * (self.left.strength - self.right.strength)
        )

        current_edge: RayInteractorEdge = points_sorted[0][2]
        next_current_edge: RayInteractorEdge | None = None

        active_edges: set[RayInteractorEdge] = {current_edge}
        collecting_rays: bool = points_sorted[0][0] == right_sink

        for end, start, edge in points_sorted[1:]:
            print("===")
            # print("start:", start, "end:", end)
            # print("current: ", current_edge)
            # print("active: \n| - ", end="")
            # print("\n| - ".join(str(e) for e in active_edges))

            if end == right_sink:
                collecting_rays = True

            left_ray = None
            next_right_ray = None

            # Get the end fraction and strength
            end_fraction = get_intersection_fraction(
                right_sink, end_normal,
                start, beam_dir
            )

            # Get the distance from the start of the ray to the end
            edge_dist = (start - end).mag

            # Since the current edge is unlikely to be perpendicular to the beam
            # We need to find the distance from the current edge to do comparisons
            current_intersection = get_intersection(
                current_edge.start, current_edge.direction,
                start, beam_dir
            )
            current_intersection_depth = (current_intersection - start).mag
            # current_intersection_depth = float('inf')

            if edge in active_edges:
                # This edge is ending, so we want to make a new beam
                active_edges.discard(edge)
                starting = False
            else:
                # The edge is starting, so we want to see if it is in front of or behind the current edge
                active_edges.add(edge)
                starting = True

            # If the edge is behind the current edge we can just skip it for now
            if edge_dist > current_intersection_depth:
                continue

            if starting:
                # We are starting a new edge, and this edge is the closest edge.

                # This means we can use the current_intersection to create a new ray
                left_ray = Ray(
                    start,
                    beam_dir,
                    current_intersection_depth,
                    self.right.strength + end_fraction * (self.left.strength - self.right.strength)
                )

                next_right_ray = Ray(
                    start,
                    beam_dir,
                    edge_dist,
                    self.right.strength + end_fraction * (self.left.strength - self.right.strength)
                )

                current_edge = edge
            else:
                # We are ending an edge. This will always be the active edge.
                left_ray = Ray(
                    start,
                    beam_dir,
                    edge_dist,
                    self.right.strength + end_fraction * (self.left.strength - self.right.strength)
                )

                if end != left_sink:
                    next_edge = None
                    closest_dist = float('inf')

                    for edge_ in active_edges:
                        intersection = get_intersection(
                            edge_.start, edge_.direction,
                            start, beam_dir
                        )
                        intersection_dist = (intersection - start).mag
                        if intersection_dist < closest_dist:
                            next_edge = edge_
                            closest_dist = intersection_dist

                    assert next_edge is not None, "AHHHH There should always be at least one edge in active edges."
                    current_edge = next_edge
                    next_right_ray = Ray(
                        start,
                        beam_dir,
                        closest_dist,
                        self.right.strength + end_fraction * (self.left.strength - self.right.strength)
                    )

            # Create a beam using the left and right rays, as well as the current edge.
            if collecting_rays and left_ray is not None:
                new_beam = BeamLightRay(
                    self.colour,
                    left_ray,
                    right_ray
                )
                left_intersection = left_ray.source + beam_dir * left_ray.length
                right_intersection = right_ray.source + beam_dir * right_ray.length

                finalised_beams.append((new_beam, current_edge, left_intersection, right_intersection))

            if end == left_sink:
                break

            if next_right_ray is not None:
                right_ray = next_right_ray

            if next_current_edge is not None:
                current_edge = next_current_edge

        return tuple(finalised_beams)