from typing import NamedTuple
from arcade.types import Color, RGBANormalized


class LuxColour(NamedTuple):
    red: bool
    green: bool
    blue: bool

    def to_int_color(self) -> Color:
        return Color(
            self.red * 255,
            self.green * 255,
            self.blue * 255,
            255
        )

    def to_float_color(self) -> RGBANormalized:
        return self.to_int_color().normalized
