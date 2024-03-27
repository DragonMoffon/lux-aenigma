from arcade import View, Text
import arcade
from pyglet.graphics import Batch


class DevMenu:
    def __init__(self, views: dict[str, View]):
        self.views = views
        self._selected = 0

        self.batch = Batch()
        self.texts: list[Text] = []
        self.instructions = Text("[UP/DOWN]: Scroll, [ENTER]: Select", 1275, 5, font_name = "GohuFont 11 Nerd Font Mono", font_size = 22, batch = self.batch, anchor_y = "bottom", anchor_x = "right")

        label_bottom = arcade.get_window().height - 5
        for k in self.views:
            t = Text(k, 5, label_bottom, font_name = "GohuFont 11 Nerd Font Mono", font_size = 22, batch = self.batch, anchor_y = "top")
            label_bottom = t.bottom - 5
            self.texts.append(t)

        self.texts[0].color = (255, 255, 0)

    @property
    def selected(self) -> int:
        return self._selected

    @selected.setter
    def selected(self, v: int):
        self.texts[self._selected].color = (255, 255, 255)
        self._selected = v % len(self.views)
        self.texts[self._selected].color = (255, 255, 0)

    @property
    def current_view(self) -> View:
        return list(self.views.values())[self.selected]

    def draw(self):
        self.batch.draw()
