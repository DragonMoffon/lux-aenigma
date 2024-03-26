from typing import TYPE_CHECKING

from lux.lux_window import LuxWindow

if TYPE_CHECKING:
    pass

_lux_window: LuxWindow = None


def get_window() -> LuxWindow:
    global _lux_window
    if _lux_window is None:
        _lux_window = LuxWindow()
    return _lux_window
