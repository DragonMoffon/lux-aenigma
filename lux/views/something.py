from pyglet.math import Vec2

from lux.engine.colour import LuxColour
from lux.engine.debug import DebugRenderer
from lux.engine.debug.ray_renderer import RayDebugRenderer
from lux.engine.lights.ray import Ray
from lux.lib.view import LuxView


class SomethingView(LuxView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ray = Ray(Vec2(100, 100), Vec2(1, 0), 100.0, LuxColour(True, False, False))

        self.renderer = DebugRenderer()
        self.ray_renderer = RayDebugRenderer(self.ray)
        self.renderer.append(self.ray_renderer)

    def on_draw(self):
        self.clear()
        self.renderer.draw()
