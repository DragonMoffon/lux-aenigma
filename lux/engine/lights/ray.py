from __future__ import annotations
from typing import NamedTuple, TYPE_CHECKING

from pyglet.math import Vec2

from lux.engine.colour import LuxColour
from lux.util.maths import Direction, get_intersection, get_segment_intersection
from lux.engine.interactors.interactor_edge import RayInteractorEdge
if TYPE_CHECKING:
    from lux.engine.interactors.ray_interactor import RayInteractor


class Ray(NamedTuple):
    source: Vec2
    direction: Vec2
    length: float
    colour: LuxColour

    def change_source(self, new_source: Vec2):
        return Ray(new_source, self.direction, self.length, self.colour)

    def change_direction(self, new_dir: Vec2):
        return Ray(self.source, new_dir, self.length, self.colour)

    def change_length(self, new_length: float):
        return Ray(self.source, self.direction, new_length, self.colour)


class LightRay:

    def __init__(self, origin: Vec2, direction: Direction, strength: float, colour: LuxColour):
        self.origin: Vec2 = origin
        self.direction: Direction = direction
        self.strength: float = strength
        self.colour: LuxColour = colour

        self.children: set[LightRay] = set()

    def __str__(self):
        raise NotImplementedError()

    def __repr__(self):
        return self.__str__()

    def add_child(self, new_child: LightRay):
        self.children.add(new_child)

    def remove_child(self, child: LightRay):
        self.children.remove(child)
        child.kill()

    def kill(self):
        self.propagate_kill()
        self._kill()

    def propagate_kill(self):
        # a.k.a purple guy method. (Thanks digi)
        for child in self.children:
            child.kill()
            self.remove_child(child)

    def _kill(self):
        raise NotImplementedError()

    def propagate_ray(self, edge_to_interactor_map: dict[RayInteractorEdge, RayInteractor]) -> tuple[LightRay, ...]:
        self.propagate_kill()
        subdivided_ray = self._propagate(edge_to_interactor_map)
        children = ()
        for child in subdivided_ray:
            children += child.propagate_ray(edge_to_interactor_map)

        return children

    def _propagate(self, edge_to_interactor_map: dict[RayInteractorEdge, RayInteractor]) -> tuple[LightRay, ...]:
        raise NotImplementedError()


class BeamLightRay(LightRay):
    """
    When a light ray is completely parallel it makes finding the intersections much easier
    """

    def __init__(self, origin: Vec2, direction: Direction, strength: float, colour: LuxColour, left: Ray, right: Ray):
        if left.direction != right.direction:
            raise ValueError("The left and right edges of a Beam should be parallel")

        if abs(direction.dot(self._left.source - self._right.source)) > 0.0:
            raise ValueError("The direction is not normal base of the Beam")

        super().__init__(origin, direction, strength, colour)
        normal = direction.to_normal()
        self.normal = normal

        self._left = left
        self._right = right

    def __str__(self):
        return f"BeamLightRay<{self.origin=}, {self._left=}, {self._right=}>"

    def _kill(self):
        self._left = None
        self._right = None

    def _generate_points(self, edges):
        left_source = self._left.source
        beam_dir = self._left.direction

        for edge in edges:
            start_point = edge.start
            end_point = edge.end

            start_intersection = get_intersection(left_source, self.normal, start_point, beam_dir)
            if start_intersection is not None:
                yield start_point, start_intersection, edge

            end_intersection = get_intersection(left_source, self.normal, end_point, beam_dir)
            if end_intersection is not None:
                yield end_point, end_intersection, edge

    def _propagate(self, edge_to_interactor_map: dict[RayInteractorEdge, RayInteractor]) -> tuple[LightRay, ...]:
        if self._left is None or self._right is None:
            raise ValueError("This Light Beam has been killed how are you propagating it?")

        # Pull out values so we don't use the dot notation so much
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
            key=lambda p, _, __: (p - right_source).dot(beam_normal)
        )

        finalised_beams: list[tuple[LightRay, RayInteractor]] = list()

        right_ray: Ray | None = None

        active_edges: set[RayInteractorEdge] = set()

        current_edge: RayInteractorEdge | None = None

        for point in points_sorted:
            print(point)

        edge_to_interactor_map.pop(end_edge)
        return ()


class PointLightRay:
    pass


class ConeLightRay:
    pass



