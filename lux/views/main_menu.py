import logging

from arcade import key

from lux.lib.dev_menu import DevMenu
from lux.lib.view import LuxView
from lux.views.something import SomethingView

logger = logging.getLogger("lux")


class MenuView(LuxView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu = DevMenu({
            "Something": SomethingView(back=self)
        })

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case key.UP:
                self.menu.selected -= 1
            case key.DOWN:
                self.menu.selected += 1
            case key.ENTER:
                self.window.show_view(self.menu.current_view)

    def on_draw(self):
        self.clear()
        self.menu.draw()
