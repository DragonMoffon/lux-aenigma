from random import random

from arcade.draw_commands import draw_line_strip, draw_points
from pyglet.math import Vec2

from lux.util.view import LuxView


class TriTestView(LuxView):

    def __init__(self, back: LuxView):
        super().__init__(back=back)

        self.tri_points = (
            Vec2(200, 300),
            Vec2(self.window.center_x, self.window.height - 100),
            Vec2(self.window.width - 200, 300),
            Vec2(200, 300)
        )
        self.tri_a = Vec2(200, 300) - Vec2(self.window.center_x, self.window.height - 100)
        self.tri_b = Vec2(self.window.width - 200, 300) - Vec2(self.window.center_x, self.window.height - 100)

        self.points = ()

        self.t = 0.0

    def on_key_press(self, symbol: int, modifiers: int):
        super().on_key_press(symbol, modifiers)

    def on_update(self, delta_time: float):
        self.t += delta_time
        if self.t >= 1.0/60.0:
            self.t -= 1.0/60.0

            n_a, n_b = random(), random()
            if n_a + n_b >= 1.0:
                n_a, n_b = 1.0-n_a, 1.0-n_b

            self.points += (Vec2(self.window.center_x, self.window.height - 100) + self.tri_a * n_a + self.tri_b * n_b,)

        return super().on_update(delta_time)


    def on_draw(self):
        self.clear()

        draw_line_strip(self.tri_points, (255, 0, 0, 255), 4)
        if self.points:
            draw_points(self.points, (0, 255, 0, 255), 2)