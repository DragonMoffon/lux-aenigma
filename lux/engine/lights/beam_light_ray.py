from __future__ import annotations
from typing import TYPE_CHECKING, Generator

from pyglet.math import Vec2

from lux.engine.lights.ray import Ray, LightRay
from lux.engine.colour import LuxColour
from lux.util.maths import Direction, get_intersection, get_segment_intersection
from lux.engine.interactors.interactor_edge import RayInteractorEdge

if TYPE_CHECKING:
    from lux.engine.interactors.ray_interactor import RayInteractor


class BeamLightRay(LightRay):
    """
    When a light ray is completely parallel it makes finding the intersections much easier
    """

    def __init__(self, origin: Vec2, direction: Direction, strength: float, colour: LuxColour, left: Ray, right: Ray):
        self._left = left
        self._right = right

        if left.direction != right.direction:
            raise ValueError("The left and right edges of a Beam should be parallel")

        if abs(direction.dot(self._left.source - self._right.source)) > 0.0:
            raise ValueError("The direction is not normal base of the Beam")

        super().__init__(origin, direction, strength, colour)
        normal = direction.to_normal()
        self.normal = normal

    def __str__(self):
        return f"BeamLightRay<{self.origin=}, {self._left=}, {self._right=}>"

    def _kill(self):
        self._left = None
        self._right = None

    def _generate_points(self, edges) -> Generator[tuple[Vec2, Vec2, RayInteractorEdge]]:
        left_source = self._left.source
        right_source = self._right.source
        beam_dir = self._left.direction
        beam_normal = Vec2(self._left.direction.y, -self._left.direction.x)
        base_normal = self.normal

        right_sink = right_source + beam_dir * self._right.length
        left_sink = left_source + beam_dir * self._left.length

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

            if ((start_point - left_source).dot(beam_normal) > 0.0) == ((end_point - right_source).dot(beam_normal) < 0.0):
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

    def _propagate(self, edge_to_interactor_map: dict[RayInteractorEdge, RayInteractor]) -> tuple[LightRay, ...]:
        if self._left is None or self._right is None:
            raise ValueError("This Light Beam has been killed how are you propagating it?")

        # Pull out values, so we don't use the dot notation so much
        right_source = self._right.source
        left_source = self._left.source
        beam_dir = self._right.direction
        beam_normal = self.normal

        right_sink = right_source + beam_dir * self._right.length
        left_sink = left_source + beam_dir * self._left.length

        end_edge = RayInteractorEdge(right_sink, left_sink, True)
        edge_to_interactor_map[end_edge] = None

        points_sorted = sorted(
            self._generate_points(edge_to_interactor_map.keys()),
            reverse=True,
            key=lambda p: (p[0] - right_source).dot(beam_normal)
        )

        finalised_beams: list[tuple[LightRay, RayInteractor, RayInteractorEdge, Vec2, Vec2]] = list()

        right_ray: Ray | None = Ray(
            points_sorted[0][1],
            beam_dir,
            (points_sorted[0][0] - points_sorted[0][1]).mag,
            self.colour
        )

        current_edge: RayInteractorEdge = points_sorted[0][2]
        last_endpoint: Vec2 | None = points_sorted[0][0]

        active_edges: set[RayInteractorEdge] = {current_edge}

        collecting_rays: bool = False

        for end, start, edge in points_sorted[1:]:
            if end == right_sink:
                collecting_rays = True

            # Get the distance from the start of the ray to the end
            edge_dist = (start - end).mag

            # Since the current edge is unlikely to be perpendicular to the beam
            # We need to find the distance from the current edge to do comparisons
            current_intersection = None
            current_intersection_depth = float('inf')
            if current_edge is not None:
                current_intersection = get_segment_intersection(
                    current_edge.start, current_edge.diff,
                    start, (end - start)
                )
                if current_intersection is not None:
                    current_intersection_depth = (current_intersection - start).mag

            if edge in active_edges:
                # This edge is ending, so we want to make a new beam
                active_edges.discard(edge)
                starting = False
            else:
                # The edge is starting, so we want to see if it is in front of or behind the current edge
                active_edges.add(edge)
                starting = True

            # If the edge is behind the current edge we can just skip it for now
            if edge_dist >= current_intersection_depth:
                continue

            if starting:
                # We are starting a new edge, and this edge is the closest edge.

                # This means we can use the current_intersection to create a new ray
                pass
            else:
                # We are ending an edge. This will always be the active edge.
                pass

        edge_to_interactor_map.pop(end_edge)
        return ()