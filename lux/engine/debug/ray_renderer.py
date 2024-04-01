from pyglet.math import Vec2
from arcade import draw_line, draw_point

from lux.engine.lights import Ray
from lux.engine.lights.beam_light_ray import BeamLightRay


_NORMAL_RAY_DIST = 15.0
_NORMAL_COLOR = (0, 255, 0, 255)
_LINE_WIDTH = 2
_POINT_SIZE = 6


def draw_ray(ray: Ray):
    colour = ray.colour.to_int_color()
    source, direction, length = ray.source, ray.direction, ray.length
    end = source + direction * length

    normal = Vec2(direction.y, -direction.x)
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
        draw_ray(self.child)


class BeamDebugRenderer:

    def __init__(self, child: BeamLightRay):
        self.child: BeamLightRay = child

    def update_child(self, new_child: BeamLightRay):
        self.child = new_child

    def draw(self):
        draw_ray(self.child._left)
        draw_ray(self.child._right)
        draw_line(*self.child._left.source, *self.child._right.source, self.child.colour.to_int_color(), _LINE_WIDTH)
