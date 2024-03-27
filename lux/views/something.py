import arcade.key
from pyglet.math import Vec2

from lux.engine.colour import LuxColour
from lux.engine.debug import DebugRenderer
from lux.engine.debug.ray_renderer import RayDebugRenderer
from lux.engine.debug.ray_interactor_renderer import RayInteractorRenderer
from lux.engine.lights.ray import Ray
from lux.engine.interactors.portal import PortalRayInteractor
from lux.engine.interactors.mirror import MirrorRayInteractor
from lux.engine.lights.ray_interaction import calculate_ray_interaction
from lux.engine.upscale_renderer import UpscaleBuffer
from lux.util.maths import Direction
from lux.util.view import LuxView


class SomethingView(LuxView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ray = Ray(Vec2(20, 45), Direction.EAST(), 1000000.0, LuxColour.RED())
        self.child_ray = None

        self.renderer = DebugRenderer()

        self.ray_renderer = RayDebugRenderer(self.ray)
        self.child_renderer = None

        self.renderer.append(self.ray_renderer)

        self._portal_a = PortalRayInteractor(100.0, Vec2(125, 200), Direction.WEST(), LuxColour.YELLOW())
        self._portal_b = PortalRayInteractor(100.0, Vec2(400, 250), Direction.NORTHEAST(), LuxColour.CYAN())
        self._mirror_a = MirrorRayInteractor(100.0, Vec2(200, 125), Direction.SOUTHWEST(), LuxColour.MAGENTA())
        self.renderer.append(RayInteractorRenderer(self._portal_a))
        self.renderer.append(RayInteractorRenderer(self._portal_b))
        self.renderer.append(RayInteractorRenderer(self._mirror_a))

        self.interactors = (self._portal_a, self._portal_b, self._mirror_a)

        self._portal_a.set_siblings(self._portal_b)

        self.upscale_renderer = UpscaleBuffer(640, 360)

        self.dir = True
        self.paused = False

    def on_update(self, delta_time: float):
        if self.paused:
            return

        if self.child_renderer is not None:
            self.renderer.remove(self.child_renderer)
            self.child_renderer = None

        ray = Ray(self.ray.source, self.ray.direction.rotate((-1 if self.dir else 1) * delta_time * 3.14159 / 20.0), 300, self.ray.colour)

        interaction = calculate_ray_interaction(ray, self.interactors)
        if interaction is None:
            self.ray = ray
            self.ray_renderer.update_child(self.ray)
            return
        intersection, edge, interactor = interaction
        base_ray = ray.change_length((intersection - ray.source).mag)
        child_ray = interactor.ray_hit(ray, edge, intersection)

        self.ray = base_ray
        self.ray_renderer.update_child(self.ray)

        if child_ray is None:
            return

        self.child_ray = child_ray
        self.child_renderer = RayDebugRenderer(child_ray)
        self.renderer.append(self.child_renderer)

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case arcade.key.ENTER:
                self.dir = not self.dir
            case arcade.key.SPACE:
                self.paused = not self.paused

    def on_draw(self):
        self.clear()
        with self.upscale_renderer.activate() as ur:
            ur.clear()
            self.renderer.draw()
        self.upscale_renderer.draw()
