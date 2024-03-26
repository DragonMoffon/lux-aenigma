from pyglet.math import Vec2

from lux.engine.lights import Ray
from lux.engine.interactors import RayInteractorEdge, RayInteractor
from lux.engine.color import LuxColour


class PortalRayInteractor(RayInteractor):

    def __init__(self, height: float, origin: Vec2, direction: Vec2, colour: LuxColour):
        bounds = (
            RayInteractorEdge(
                Vec2(0.0, -height/2.0),
                Vec2(0.0, height/2.0),
                False
            ),
        )
        super().__init__(origin, direction, colour, bounds)
        self._sibling: PortalRayInteractor = None

    def set_siblings(self, sibling):
        self._sibling, sibling._sibling = sibling, self

    def ray_hit(self, in_ray: Ray, in_edge: RayInteractorEdge, intersection_point: Vec2) -> Ray | None:
        if self._sibling is None:
            return

        ray_direction = in_ray.direction
        sibling_normal = self._sibling.direction

        if ray_direction.dot(sibling_normal) > 0.0:
            return None


