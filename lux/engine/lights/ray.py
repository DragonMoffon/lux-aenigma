from __future__ import annotations
from typing import NamedTuple, TYPE_CHECKING

from pyglet.math import Vec2

from lux.engine.colour import LuxColour
from lux.util.maths import Direction
if TYPE_CHECKING:
    from lux.engine.interactors.interactor_edge import RayInteractorEdge
    from lux.engine.interactors.ray_interactor import RayInteractor


class Ray(NamedTuple):
    source: Vec2
    direction: Vec2
    length: float
    colour: LuxColour

    def __eq__(self, other: Ray):
        return self.source == other.source and self.direction == other.direction and self.length == other.colour

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


class ConeLightRay(LightRay):
    pass



