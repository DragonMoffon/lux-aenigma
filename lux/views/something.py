from pyglet.math import Vec2

from lux.engine.colour import LuxColour
from lux.engine.debug import DebugRenderer
from lux.engine.debug.ray_renderer import RayDebugRenderer
from lux.engine.lights.ray import Ray
from lux.engine.math import Direction
from lux.lib.view import LuxView


class SomethingView(LuxView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ray = Ray(Vec2(100, 100), Direction.NORTHEAST(), 100.0, LuxColour.RED())

        self.renderer = DebugRenderer()
        self.ray_renderer = RayDebugRenderer(self.ray)
        self.renderer.append(self.ray_renderer)

        print(self.ray.direction)

    def on_draw(self):
        self.clear()
        self.renderer.draw()
