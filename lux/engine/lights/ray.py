from __future__ import annotations
from logging import getLogger
from typing import NamedTuple, TYPE_CHECKING

from pyglet.math import Vec2

from lux.engine.colour import LuxColour
if TYPE_CHECKING:
    from lux.engine.interactors import RayInteractor, RayInteractorEdge

logger = getLogger("lux")


class Ray(NamedTuple):
    source: Vec2
    direction: Vec2
    length: float
    strength: float

    def __eq__(self, other: Ray):
        return (
                self.source == other.source
                and
                self.direction == other.direction
                and
                self.length == other.length
                and
                self.strength == other.strength
        )

    def change_source(self, new_source: Vec2):
        return Ray(new_source, self.direction, self.length, self.strength)

    def change_direction(self, new_dir: Vec2):
        return Ray(self.source, new_dir, self.length, self.strength)

    def change_length(self, new_length: float):
        return Ray(self.source, self.direction, new_length, self.strength)

    def change_strength(self, new_strength: float):
        return Ray(self.source, self.direction, self.length, new_strength)

    def __str__(self) -> str:
        return f"Ray<({round(self.source.x, 3)}, {round(self.source.y, 3)}), dir ({round(self.direction.x, 3)}, {round(self.direction.y, 3)}), len {self.length}, str {self.strength}>"


class LightRay:

    def __init__(self, origin: Vec2, direction: Vec2, colour: LuxColour, left: Ray, right: Ray):
        self.origin: Vec2 = origin
        self.direction: Vec2 = direction
        self.colour: LuxColour = colour

        self.left: Ray = left
        self.right: Ray = right

        self.children: set[LightRay] = set()

    def __str__(self):
        raise NotImplementedError()

    def __repr__(self):
        return self.__str__()

    def add_child(self, new_child: LightRay):
        self.children.add(new_child)

    def add_children(self, children: tuple[LightRay, ...]):
        self.children.update(children)

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
        logger.debug(f"{self}: Propogating!")
        self.propagate_kill()
        kids = 0
        replacements = self._propagate(edge_to_interactor_map)
        for child, edge, left_intersection, right_intersection in replacements:
            logger.info(f"{kids}")
            kids += 1
            interactor = edge_to_interactor_map.get(edge)
            if interactor is None:
                continue

            sub_children = interactor.ray_hit(child, edge, left_intersection, right_intersection)
            for sub_child in sub_children:
                logger.debug(sub_child.colour)
                # child.add_child(sub_child)
                child.add_children(sub_child.propagate_ray(edge_to_interactor_map))

        return tuple(child[0] for child in replacements)

    def _propagate(self, edge_to_interactor_map: dict[RayInteractorEdge, RayInteractor]) -> tuple[tuple[LightRay, RayInteractorEdge, Vec2, Vec2], ...]:
        raise NotImplementedError()


class ConeLightRay(LightRay):
    pass
