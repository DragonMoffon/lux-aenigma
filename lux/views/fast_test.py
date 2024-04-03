from logging import getLogger
from timeit import timeit

import arcade
from pyglet.math import Vec2

from lux.util.view import LuxView
from lux.util.maths import Direction
from lux.engine.colour import LuxColour
from lux.engine.lights.ray import Ray
from lux.engine.lights.beam_light_ray import BeamLightRay
from lux.engine.interactors.interactor_edge import RayInteractorEdge
from lux.engine.interactors.ray_interactor import RayInteractor
from lux.engine.interactors.filter import FilterRayInteractor
from lux.util.maths import get_segment_intersection, get_intersection, get_segment_intersection_fraction, get_intersection_fraction
from lux.engine.debug import DebugRenderer
from lux.engine.debug.ray_interactor_renderer import RayInteractorRenderer
from lux.engine.debug.ray_renderer import BeamDebugRenderer

logger = getLogger("lux")


def find_beam_edge_map(interactors, parent,
                       left_source, left_sink,
                       right_source, right_sink,
                       beam_dir, beam_normal,
                       origin_dir, origin_normal) -> tuple[dict[RayInteractorEdge, RayInteractor], list[tuple[Vec2, float, Vec2, RayInteractorEdge]]]:
    edge_to_interactor_map = dict()
    edge_points = []

    # Start by generating the adjusted edge, and clamping it to the bounds of the beam.
    # Then for the start and end
    for interactor in interactors:
        if interactor == parent:
            continue

        origin = interactor.origin
        heading = interactor.direction.heading

        for original_edge in interactor.bounds:
            start_point = origin + original_edge.start.rotate(heading)
            end_point = origin + original_edge.end.rotate(heading)
            edge_diff = end_point - start_point

            # Pre-calc some diffs that are used for bounds checking.
            start_left = (start_point - left_sink)
            end_left = (end_point - left_sink)
            start_right = (start_point - right_source)
            end_right = (end_point - right_source)

            # First check if the edge aligns with the beam. We want to ignore this edge case.
            if abs(original_edge.direction.dot(beam_dir)) == 1.0:
                continue

            # Secondly check if the edge is behind the beam. In this case we can ignore it
            if start_right.dot(origin_dir) <= 0.0 and end_right.dot(origin_dir) <= 0.0:
                continue

            # Third check if the edge is ahead of the beam. In this case we can ignore it.
            if start_left.dot(beam_dir) >= 0.0 and end_left.dot(beam_dir) >= 0.0:
                continue

            is_start_in_beam = ((start_right.dot(origin_dir) > 0.0) and (start_left.dot(beam_dir) < 0.0) and
                                (start_left.dot(beam_normal) > 0.0) == (start_right.dot(beam_normal) < 0.0))

            is_end_in_beam = ((end_right.dot(origin_dir) > 0.0) and (end_left.dot(beam_dir) < 0.0) and
                              (end_left.dot(beam_normal) > 0.0) == (end_right.dot(beam_normal) < 0.0))

            # Both the start and end are in the beam so we can skip all the intersection checks.
            if is_start_in_beam and is_end_in_beam:
                start_final = start_point
                end_final = end_point

                start_intersection_point = get_intersection(start_final, beam_dir, right_source, origin_normal)
                end_intersection_point = get_intersection(end_final, beam_dir, right_source, origin_normal)

                start_diff = start_final - start_intersection_point
                end_diff = end_final - end_intersection_point

                edge_final = RayInteractorEdge(start_point, end_point, original_edge.bi_dir)
                edge_to_interactor_map[edge_final] = interactor
            else:
                # Fourth find if the edge intersects the right edge of the beam.
                right_intersection = get_segment_intersection_fraction(start_point, end_point, right_source, right_sink)
                right_start = right_source

                # Fifth find if the edge intersects the right edge of the beam.
                left_intersection = get_segment_intersection_fraction(start_point, end_point, left_source, left_sink)
                left_start = left_source

                # Sixth find if the edge intersects the base of the beam.
                start_intersection = get_segment_intersection_fraction(start_point, end_point, right_source, left_source)
                start_start = None if start_intersection is None else start_point + edge_diff * start_intersection

                # Seventh find if the edge intersects the end of the beam.
                end_intersection = get_segment_intersection_fraction(start_point, end_point, right_sink, left_sink)
                end_start = None

                intersections = sorted(filter(lambda i: i[0] is not None, ((right_intersection, right_start), (left_intersection, left_start), (start_intersection, start_start), (end_intersection, None))))

                if not intersections:
                    # Because there are no intersections the edge is outside the beam
                    continue
                elif len(intersections) == 1:
                    # There is one intersection
                    if is_start_in_beam:
                        start_final = start_point
                        start_intersection_point = None

                        intersection_fraction, end_intersection_point = intersections[0]

                        end_final = start_point + edge_diff * intersection_fraction
                    else:
                        end_final = end_point
                        end_intersection_point = None

                        intersection_fraction, start_intersection_point = intersections[0]
                        start_final = start_point + edge_diff * intersection_fraction
                else:
                    # There are two or more intersections.
                    # In fact there are exactly two intersections.
                    # If there are more than two, that means the edge hits a corner.
                    # In this case multiple intersections will be equal, and it does not matter.

                    start_fraction, start_intersection_point = intersections[0]
                    end_fraction, end_intersection_point = intersections[-1]

                    start_final = start_point + edge_diff * start_fraction
                    end_final = start_point + edge_diff * end_fraction

                # Make an edge out of the final start and end points
                edge_final = RayInteractorEdge(start_final, end_final, original_edge.bi_dir)
                edge_to_interactor_map[edge_final] = interactor

                # Find the intersection with the front of the beam, and the distance from that point
                if start_intersection_point is None:
                    start_intersection_point = get_intersection(right_source, origin_normal, start_final, beam_dir)

                if end_intersection_point is None:
                    end_intersection_point = get_intersection(right_source, origin_normal, end_final, beam_dir)

                start_diff = start_final - start_intersection_point
                end_diff = end_final - end_intersection_point

            edge_points.append((start_final, start_diff.dot(start_diff), start_intersection_point, edge_final))
            edge_points.append((end_final, end_diff.dot(end_diff), end_intersection_point, edge_final))
    return edge_to_interactor_map, edge_points


def find_intersections(interactors: tuple[RayInteractor, ...], beam: BeamLightRay, parent: RayInteractor = None):
    logger.info("Getting intersections")
    beam_colour = beam.colour

    left_source = beam.left.source
    left_strength = beam.left.strength
    right_source = beam.right.source
    right_strength = beam.right.strength
    beam_dir = beam.left.direction
    beam_normal = Vec2(beam.left.direction.y, -beam.left.direction.x)
    origin_dir = beam.direction
    origin_normal = beam.normal

    right_sink: Vec2 = right_source + beam_dir * beam.right.length
    left_sink: Vec2 = left_source + beam_dir * beam.left.length
    end_width: float = (left_sink - right_sink).mag
    end_normal: Vec2 = (left_sink - right_sink) / end_width

    edge_to_interactor_map, edge_points = find_beam_edge_map(interactors, parent,
                                                             left_source, left_sink,
                                                             right_source, right_sink,
                                                             beam_dir, beam_normal,
                                                             origin_dir, origin_normal)

    back_edge = RayInteractorEdge(right_sink, left_sink, True)
    edge_to_interactor_map[back_edge] = None
    edge_points.append((right_sink, beam.right.length**2, right_source, back_edge))
    edge_points.append((left_sink, beam.left.length**2, left_source, back_edge))

    if len(edge_points) == 2:
        return [(beam, back_edge, right_sink, left_sink)], edge_to_interactor_map

    # Sort every point from left to right, breaking ties by depth
    sorted_points = sorted(edge_points, key=lambda p: ((right_source - p[2]).dot(beam_normal), p[1]))

    logger.info("\n".join(f"{(right_source - p[2]).dot(beam_normal)}: {p}" for p in sorted_points))

    end_fraction = get_intersection_fraction(
        right_sink, end_normal,
        sorted_points[0][2], beam_dir
    )

    current_edge: RayInteractorEdge = sorted_points[0][-1]
    right_ray: Ray = Ray(
        sorted_points[0][2],
        beam_dir,
        sorted_points[0][1]**0.5,
        right_strength + end_fraction * (left_strength - right_strength)
    )

    active_edges: set[RayInteractorEdge] = {current_edge}
    incomplete_edges: set[RayInteractorEdge] = set(edge_to_interactor_map.keys())
    finalised_beams: list[tuple[BeamLightRay, RayInteractorEdge, Vec2, Vec2]] = []

    """test_dict = dict()
    for end, length_sqr, start, edge in sorted_points:
        edge_values = test_dict.get(edge, [])
        edge_values.append((length_sqr, start, end))
        test_dict[edge] = edge_values

    for edge, values in test_dict.items():
        print(edge, values)
        right_len, right_start, right_end = values[0]
        left_len, left_start, left_end = values[-1]

        right_ray = Ray(
            right_start,
            beam_dir,
            right_len**0.5,
            right_len**0.5
        )

        left_ray = Ray(
            left_start,
            beam_dir,
            left_len**0.5,
            left_len**0.5
        )

        finalised_beams.append((BeamLightRay(beam_colour, left_ray, right_ray), edge, left_end, right_end))"""

    for end, length_sqr, start, edge in sorted_points[1:]:
        logger.info(f"Next Point: {start} : {end}")
        left_ray = None
        next_right_ray = None
        next_current_edge = None

        if edge in active_edges:
            # This edge is ending
            active_edges.discard(edge)
            starting = False

            incomplete_edges.discard(edge)
        else:
            # The edge is starting
            active_edges.add(edge)
            starting = True

        logger.debug(f"{edge}")
        logger.debug(f"{current_edge}")
        logger.debug(f"{active_edges}")

        # Since the current edge is unlikely to be perpendicular to the beam
        # We need to find the distance from the current edge to do comparisons
        current_intersection = get_intersection(
            current_edge.start, current_edge.direction,
            start, beam_dir
        )
        current_diff = (start - current_intersection)

        if current_diff.dot(current_diff) < length_sqr and edge != current_edge:
            continue

        # Get the end fraction and strength
        end_fraction = get_intersection_fraction(
            right_sink, (left_sink - right_sink),
            start, beam_dir
        )
        end_strength = right_strength + end_fraction * (left_strength - right_strength)

        if starting:
            # In the case the edge just started then we can easily calc the next ray.
            left_ray = Ray(
                start,
                beam_dir,
                current_diff.mag,
                end_strength
            )

            next_right_ray = Ray(
                start,
                beam_dir,
                length_sqr**0.5,
                end_strength
            )

            next_current_edge = edge
        else:
            left_ray = Ray(
                start,
                beam_dir,
                length_sqr**0.5,
                end_strength
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
                next_current_edge = next_edge
                next_right_ray = Ray(
                    start,
                    beam_dir,
                    closest_dist,
                    end_strength
                )

        logger.debug(next_current_edge)
        if left_ray is not None:
            logger.debug("making a new beam")
            new_beam = BeamLightRay(
                beam_colour,
                left_ray,
                right_ray
            )
            left_intersection = left_ray.source + beam_dir * left_ray.length
            right_intersection = right_ray.source + beam_dir * right_ray.length

            finalised_beams.append((new_beam, current_edge, left_intersection, right_intersection))

            right_ray = next_right_ray
            current_edge = next_current_edge

        if start == left_source:
            break

    return finalised_beams, edge_to_interactor_map


def propogate_beam(interactors: tuple[RayInteractor, ...], beam: BeamLightRay, parent: RayInteractor = None):
    kids = 0
    replacements, edge_map = find_intersections(interactors, beam, parent)
    for child, edge, left_intersection, right_intersection in replacements:
        kids += 1
        interactor = edge_map.get(edge)
        if interactor is None:
            continue

        sub_children = interactor.ray_hit(child, edge, left_intersection, right_intersection)
        for sub_child in sub_children:
            child.add_children(propogate_beam(interactors, sub_child, interactor))

    return tuple(child[0] for child in replacements)


ONE_FRAME = 1/600


class FastTestView(LuxView):

    def __init__(self, back: LuxView):
        super().__init__(back=back)
        w, h = self.window.center

        self.renderer = DebugRenderer()

        self.offset = Vec2(0.0, 150.0)
        self.cen = Vec2(w, h)
        self.beam = BeamLightRay(
            LuxColour.WHITE(),
            Ray(self.cen + self.offset.rotate(0.0), Direction.EAST().rotate(0.0), 500.0, 500.0),
            Ray(self.cen - self.offset.rotate(0.0), Direction.EAST().rotate(0.0), 500.0, 500.0)
        )
        self.t = 0.0

        self.filter_red = FilterRayInteractor(Vec2(w+125, h+75), Direction.NORTHWEST(), LuxColour.RED(), (RayInteractorEdge(Vec2(0.0, -250.0), Vec2(0.0, 250.0), True),))
        self.filter_green = FilterRayInteractor(Vec2(w+400, h+25), Direction.WEST(), LuxColour.GREEN(), (RayInteractorEdge(Vec2(0.0, -50.0), Vec2(0.0, 50.0), True),))
        self.filter_blue = FilterRayInteractor(Vec2(w+200, h-75), Direction.WEST(), LuxColour.BLUE(), (RayInteractorEdge(Vec2(0.0, -50.0), Vec2(0.0, 50.0), True),))
        self.filter_cyan_a = FilterRayInteractor(Vec2(w+100, h-35), Direction.NORTHWEST(), LuxColour.CYAN(), (RayInteractorEdge(Vec2(0.0, -25.0), Vec2(0.0, 25.0), False),))
        self.filter_cyan_b = FilterRayInteractor(Vec2(w+150, h-125), Direction.WEST(), LuxColour.CYAN(), (RayInteractorEdge(Vec2(0.0, -50.0), Vec2(0.0, 50.0), False),))

        self.interactors = (self.filter_red, self.filter_green, self.filter_blue, self.filter_cyan_a, self.filter_cyan_b)

        self.points = ()

        self.rerender()
        # t = (timeit(lambda: find_intersections(self.interactors, self.beam), number=10000) / 10000)
        # print(1 / t)
        # print(1 / t / 60)

        self.rev = False
        self.paused = False

        self.speed = 0.01
        self.turbo = False

    def rerender(self):
        self.renderer.clear()

        for interactor in self.interactors:
            self.renderer.append(RayInteractorRenderer(interactor))
        # self.renderer.append(BeamDebugRenderer(self.beam))

        left_source = self.beam.left.source
        right_source = self.beam.right.source
        beam_dir = self.beam.left.direction
        beam_normal = Vec2(self.beam.left.direction.y, -self.beam.left.direction.x)
        origin_dir = self.beam.direction
        origin_normal = self.beam.normal
        right_sink: Vec2 = right_source + beam_dir * self.beam.right.length
        left_sink: Vec2 = left_source + beam_dir * self.beam.left.length

        _, self.points = find_beam_edge_map(
            self.interactors, None,
            left_source, left_sink,
            right_source, right_sink,
            beam_dir, beam_normal,
            origin_dir, origin_normal
        )

        beams = propogate_beam(self.interactors, self.beam)
        def add_beam(beam):
            self.renderer.append(BeamDebugRenderer(beam))
            for child in beam.children:
                add_beam(child)
        for beam in beams:
            add_beam(beam)

    def shift_beam(self, delta_time: float):
        self.t += delta_time * self.speed * (-1 if self.rev else 1.0) * (10 if self.turbo else 1)

        angle = (self.t % 1.0) * 2.0 * 3.1415926
        self.beam = BeamLightRay(
            LuxColour.WHITE(),
            Ray(self.cen + self.offset.rotate(angle), Direction.EAST().rotate(angle), 500.0, 500.0),
            Ray(self.cen - self.offset.rotate(angle), Direction.EAST().rotate(angle), 500.0, 500.0)
        )

        self.rerender()

    def on_update(self, delta_time: float):
        # return
        if self.paused:
            return

        self.shift_beam(delta_time)

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case arcade.key.ENTER:
                self.rev = not self.rev
            case arcade.key.SPACE:
                self.paused = not self.paused
                if self.paused:
                    self.rerender()
            case arcade.key.UP:
                self.t += ONE_FRAME
                if self.paused:
                    self.shift_beam(1/60)
            case arcade.key.DOWN:
                self.t -= ONE_FRAME
                if self.paused:
                    self.shift_beam(1/60)
            case arcade.key.NUM_MULTIPLY:
                self.turbo = True

    def on_key_release(self, symbol: int, modifiers: int):
        match symbol:
            case arcade.key.NUM_MULTIPLY:
                self.turbo = False

    def on_draw(self):
        self.clear()
        self.renderer.draw()

        if self.points:
            arcade.draw_points(
                tuple(p[0] for p in self.points),
                self.beam.colour.to_int_color(),
                10
            )
