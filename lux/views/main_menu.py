import logging
from typing import Optional, Type

from arcade.experimental.input import ActionState

from util.dev_menu import DevMenu
from lux.util import LuxView
from lux.views.level_test import LevelTestView
from lux.views.musicmixer import MusicMixerView
from lux.views.fast_test import FastTestView
from lux.views.player import PlayerTestView
from lux.views.sevensegtest import SevenSegTestView

try:
    from lux.views.march_square_view import SquareView
except ModuleNotFoundError:
    SquareView = None


from time import time

logger = logging.getLogger("lux")


def load_views(unloaded: dict[str, Type[LuxView]], back: Optional[LuxView]) -> dict[str, LuxView]:
    d = {}
    for s, v in unloaded.items():
        t = time()
        loaded = v(back=back)
        logger.debug(f"{s}: {time() - t:.3f}s")
        d[s] = loaded
    return d


class MenuView(LuxView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        views: dict[str, Type[LuxView]] = {
            "Level Test": LevelTestView,
            "Light Test": FastTestView,
            "Player": PlayerTestView,
            # "Music": MusicMixerView,
            "Seven Segment Display": SevenSegTestView
        }

        if SquareView is not None:
            views["Square"] = SquareView

        loaded = load_views(views, self)
        self.menu = DevMenu(loaded)

    def on_action(self, action, state):
        if state == ActionState.RELEASED:
            return

        match action:
            case "gui_down":
                self.menu.selected += 1
            case "gui_prev":
                self.menu.selected -= 1
            case "gui_up":
                self.menu.selected -= 1
            case "gui_next":
                self.menu.selected += 1
            case "gui_select":
                self.window.show_view(self.menu.current_view)

    def on_draw(self):
        self.clear()
        self.menu.draw()
