from __future__ import annotations

from typing import NamedTuple
from arcade.types import Color, RGBANormalized

from util.classproperty import classproperty


class LuxColour(NamedTuple):
    red: bool
    green: bool
    blue: bool

    def __eq__(self, other: LuxColour):
        return self.red == other.red and self.green == other.green and self.blue == other.blue

    def to_int_color(self, alpha = 255) -> Color:
        return Color(
            self.red * 255,
            self.green * 255,
            self.blue * 255,
            alpha
        )

    def to_float_color(self, alpha=1.0) -> RGBANormalized:
        c = self.to_int_color().normalized
        return (c[0], c[1], c[2], alpha)

    def mask(self, other: LuxColour) -> LuxColour:
        return LuxColour(self.red and other.red, self.green and other.green, self.blue and other.blue)

    def invert(self):
        return LuxColour(not self.red, not self.blue, not self.green)

    @property
    def name(self) -> str:
        colour = "MISSINGNO"  # Thanks DIGI
        match (self.red, self.green, self.blue):
            case (True, True, True):
                colour = "WHITE"
            case (True, True, False):
                colour = "YELLOW"
            case (True, False, True):
                colour = "MAGENTA"
            case (True, False, False):
                colour = "RED"
            case (False, True, True):
                colour = "CYAN"
            case (False, True, False):
                colour = "GREEN"
            case (False, False, True):
                colour = "BLUE"
            case (False, False, False):
                colour = "BLACK"
        return colour

    def __repr__(self) -> str:
        return f"LuxColour({self.name})"

    @classproperty
    def WHITE(cls) -> LuxColour:
        return cls(True, True, True)

    @classproperty
    def RED(cls) -> LuxColour:
        return cls(True, False, False)

    @classproperty
    def GREEN(cls) -> LuxColour:
        return cls(False, True, False)

    @classproperty
    def BLUE(cls) -> LuxColour:
        return cls(False, False, True)

    @classproperty
    def YELLOW(cls) -> LuxColour:
        return cls(True, True, False)

    @classproperty
    def MAGENTA(cls) -> LuxColour:
        return cls(True, False, True)

    @classproperty
    def CYAN(cls) -> LuxColour:
        return cls(False, True, True)

    @classproperty
    def BLACK(cls) -> LuxColour:
        return cls(False, False, False)
