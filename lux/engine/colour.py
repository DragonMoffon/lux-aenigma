from __future__ import annotations

from typing import NamedTuple
from arcade.types import Color, RGBANormalized


class LuxColour(NamedTuple):
    red: bool
    green: bool
    blue: bool

    def __eq__(self, other: LuxColour):
        return self.red == other.red and self.green == other.green and self.blue == other.blue

    def to_int_color(self) -> Color:
        return Color(
            self.red * 255,
            self.green * 255,
            self.blue * 255,
            255
        )

    def to_float_color(self) -> RGBANormalized:
        return self.to_int_color().normalized

    def mask(self, other: LuxColour) -> LuxColour:
        return LuxColour(self.red and other.red, self.green and other.green, self.blue and other.blue)

    def invert(self):
        return LuxColour(not self.red, not self.blue, not self.green)

    def __repr__(self) -> str:
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
        return f"LuxColour({colour})"

    @classmethod
    def WHITE(cls) -> LuxColour:
        return cls(True, True, True)

    @classmethod
    def RED(cls) -> LuxColour:
        return cls(True, False, False)

    @classmethod
    def GREEN(cls) -> LuxColour:
        return cls(False, True, False)

    @classmethod
    def BLUE(cls) -> LuxColour:
        return cls(False, False, True)

    @classmethod
    def YELLOW(cls) -> LuxColour:
        return cls(True, True, False)

    @classmethod
    def MAGENTA(cls) -> LuxColour:
        return cls(True, False, True)

    @classmethod
    def CYAN(cls) -> LuxColour:
        return cls(False, True, True)

    @classmethod
    def BLACK(cls) -> LuxColour:
        return cls(False, False, False)
