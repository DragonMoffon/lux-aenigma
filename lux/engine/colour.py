from __future__ import annotations

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

    def mask(self, other: LuxColour) -> LuxColour:
        return LuxColour(self.red & other.red, self.green & other.green, self.blue & other.blue)

    def __repr__(self) -> str:
        colour = "MISSINGNO"
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
        return f"LuxColor({colour})"

    @classmethod
    def WHITE(cls) -> LuxColour:
        return LuxColour(True, True, True)

    @classmethod
    def RED(cls) -> LuxColour:
        return LuxColour(True, False, False)

    @classmethod
    def GREEN(cls) -> LuxColour:
        return LuxColour(False, True, False)

    @classmethod
    def BLUE(cls) -> LuxColour:
        return LuxColour(False, False, True)

    @classmethod
    def YELLOW(cls) -> LuxColour:
        return LuxColour(True, True, False)

    @classmethod
    def MAGENTA(cls) -> LuxColour:
        return LuxColour(True, False, True)

    @classmethod
    def CYAN(cls) -> LuxColour:
        return LuxColour(False, True, True)

    @classmethod
    def BLACK(cls) -> LuxColour:
        return LuxColour(False, False, False)
