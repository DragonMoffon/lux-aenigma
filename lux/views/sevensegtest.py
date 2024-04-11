from arcade import SpriteList
import arcade.key

from lux.engine.sevenseg import SevenSeg
from lux.util.maths import clamp
from lux.util.view import LuxView


class SevenSegTestView(LuxView):

    def __init__(self, back: LuxView):
        super().__init__(back=back)

        self.num = 0
        self.dot = False
        self.display = SevenSeg(300)
        self.display.position = self.window.center
        self.display.set_char(0)
        self.spritelist = SpriteList()
        self.spritelist.append(self.display)

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case arcade.key.UP:
                self.num += 1
                self.num = clamp(0, self.num, 15)
            case arcade.key.DOWN:
                self.num -= 1
                self.num = clamp(0, self.num, 15)
            case arcade.key.PERIOD | arcade.key.NUM_DECIMAL:
                self.dot = not self.dot
        self.display.set_char(f"{self.num:x}")
        self.display.dot = self.dot

        super().on_key_press(symbol, modifiers)

    def on_update(self, delta_time: float):
        self.display.update()
        return super().on_update(delta_time)

    def on_draw(self):
        self.clear()
        self.spritelist.draw()
