from pyglet.math import Vec2
from arcade import draw_line, draw_point, draw_polygon_filled

from lux.engine.lights import Ray
from lux.engine.lights.beam_light_ray import BeamLightRay
from lux.engine.colour import LuxColour


_NORMAL_RAY_DIST = 15.0
_NORMAL_COLOR = (0, 255, 0, 255)
_LINE_WIDTH = 2
_POINT_SIZE = 6


def draw_ray(ray: Ray, colour):
    source, direction, length = ray.source, ray.direction, ray.length
    end = source + direction * length

    normal = Vec2(-direction.y, direction.x)
    normal_end = source + normal * _NORMAL_RAY_DIST

    draw_line(source.x, source.y, end.x, end.y, colour, _LINE_WIDTH)
    draw_line(source.x, source.y, normal_end.x, normal_end.y, _NORMAL_COLOR, _LINE_WIDTH)
    draw_point(source.x, source.y, colour, _POINT_SIZE)


class RayDebugRenderer:
    def __init__(self, child: Ray):
        self.child: Ray = child

    def update_child(self, new_child: Ray):
        self.child = new_child

    def draw(self):
        draw_ray(self.child, LuxColour.WHITE())


class BeamDebugRenderer:
    def __init__(self, child: BeamLightRay):
        self.child: BeamLightRay = child

    def update_child(self, new_child: BeamLightRay):
        self.child = new_child

    def draw(self):
        draw_polygon_filled(
            (self.child.left.source, self.child.left.source + self.child.left.direction * self.child.left.length,
             self.child.right.source + self.child.right.direction * self.child.right.length, self.child.right.source),
             self.child.colour.to_int_color(127)
        )

        draw_ray(self.child.left, self.child.colour.to_int_color())
        draw_ray(self.child.right, self.child.colour.to_int_color())
        draw_line(*self.child.left.source, *self.child.right.source, self.child.colour.to_int_color(), _LINE_WIDTH)
