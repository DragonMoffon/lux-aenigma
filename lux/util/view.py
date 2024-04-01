from __future__ import annotations

from arcade import View, Window
import arcade


class LuxView(View):
    def __init__(self, window: Window | None = None, back: LuxView = None):
        super().__init__(window)
        self.back = back
        self.dirty = True

    def rerender(self):
        pass

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.BACKSPACE:
            self.window.show_view(self.back)
        return super().on_key_press(symbol, modifiers)

    def on_update(self, delta_time: float):
        if self.dirty:
            self.rerender()
            self.dirty = False
