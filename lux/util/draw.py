from arcade import draw_line
from pyglet.math import Vec2

from lux.util.colour import LuxColour


def draw_cross(origin: Vec2, size: float, colour: LuxColour = LuxColour.WHITE, thickness = 1.0):
    draw_line(
            origin.x - size, origin.y - size,
            origin.x + size, origin.y + size,
            colour.to_int_color(),
            thickness
        )
    draw_line(
        origin.x + size, origin.y - size,
        origin.x - size, origin.y + size,
        colour.to_int_color(),
        thickness
    )
