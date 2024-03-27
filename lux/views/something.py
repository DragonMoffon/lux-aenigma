from pyglet.math import Vec2

from lux.engine.colour import LuxColour
from lux.engine.debug import DebugRenderer
from lux.engine.debug.ray_renderer import RayDebugRenderer
from lux.engine.debug.ray_interactor_renderer import RayInteractorRenderer
from lux.engine.lights.ray import Ray
from lux.engine.interactors.portal import PortalRayInteractor
from lux.engine.math import Direction
from lux.engine.upscale_renderer import UpscaleBuffer
from lux.lib.view import LuxView


class SomethingView(LuxView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ray = Ray(Vec2(100, 100), Direction.NORTHEAST(), 100.0, LuxColour.RED())

        self.renderer = DebugRenderer()
        self.ray_renderer = RayDebugRenderer(self.ray)
        self.renderer.append(self.ray_renderer)

        self._portal_a = PortalRayInteractor(100.0, Vec2(300, 100), Direction.NORTH(), LuxColour.RED())
        self._portal_b = PortalRayInteractor(100.0, Vec2(150, 50), Direction.NORTHEAST(), LuxColour.BLUE())
        self.renderer.append(RayInteractorRenderer(self._portal_a))
        self.renderer.append(RayInteractorRenderer(self._portal_b))

        self._portal_a.set_siblings(self._portal_b)

        self.upscale_renderer = UpscaleBuffer(640, 360)

        print(self.ray.direction)

    def on_draw(self):
        self.clear()
        with self.upscale_renderer.activate() as ur:
            ur.clear()
            self.renderer.draw()
        self.upscale_renderer.draw()
