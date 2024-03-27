from pyglet.math import Vec2
from arcade import draw_line, draw_point

from lux.engine.lights import Ray


_NORMAL_RAY_DIST = 15.0


class RayDebugRenderer:

    def __init__(self, child: Ray):
        self._child: Ray = child

    def update_child(self, new_child: Ray):
        self._child = new_child

    def draw(self):
        colour = self._child.colour.to_int_color()
        source, direction, length = self._child.source, self._child.direction, self._child.length
        end = source + direction * length

        normal = Vec2(direction.y, -direction.x)
        normal_end = source + normal * _NORMAL_RAY_DIST

        draw_line(source.x, source.y, end.x, end.y, colour, 1)
        draw_line(source.x, source.y, normal_end.x, normal_end.y, (0, 255, 0, 255), 1)
        draw_point(source.x, source.y, colour, 4)
