from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lux.setup.lux_window import LuxWindow

_lux_window: LuxWindow = None


def set_window(window: LuxWindow):
    global _lux_window
    _lux_window = window


def get_window() -> LuxWindow:
    return _lux_window
