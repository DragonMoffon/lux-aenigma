from __future__ import annotations
from logging import getLogger
from arcade import View, Window
from arcade.experimental.input import ActionState


logger = getLogger("lux")


class LuxView(View):
    def __init__(self, window: Window | None = None, back: LuxView = None):
        super().__init__(window)
        self.back = back
        self.dirty = True

    def rerender(self):
        pass

    def go_back(self, state):
        if state == ActionState.RELEASED and self.back:
            logger.warning("forcefully going back. Improve this behavior later")
            self.window.show_view(self.back)

    def on_show_view(self):
        self.window.input_manager.subscribe_to_action("gui_back", self.go_back)

    def on_hide_view(self):
        self.window.input_manager.action_subscribers["gui_back"].discard(self.go_back)

    def on_update(self, delta_time: float):
        if self.dirty:
            self.rerender()
            self.dirty = False
