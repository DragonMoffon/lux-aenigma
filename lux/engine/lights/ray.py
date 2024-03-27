from typing import NamedTuple

from pyglet.math import Vec2

from lux.engine.colour import LuxColour


class Ray(NamedTuple):
    source: Vec2
    direction: Vec2
    length: float
    colour: LuxColour

    def change_source(self, new_source: Vec2):
        return Ray(new_source, self.direction, self.length, self.colour)

    def change_direction(self, new_dir: Vec2):
        return Ray(self.source, new_dir, self.length, self.colour)

    def change_length(self, new_length: float):
        return Ray(self.source, self.direction, new_length, self.colour)

    def change_colour(self, new_colour: LuxColour):
        return Ray(self.source, self.direction, self.length, new_colour)

    def mask(self, mask_colour: LuxColour):
        return Ray(self.source, self.direction, self.length, self.colour.mask(mask_colour))


