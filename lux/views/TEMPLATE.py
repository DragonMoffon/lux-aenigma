from lux.util.view import LuxView


class REPLACEView(LuxView):

    def __init__(self, back: LuxView):
        super().__init__(back=back)

    def on_key_press(self, symbol: int, modifiers: int):
        super().on_key_press(symbol, modifiers)

    def on_update(self, delta_time: float):
        return super().on_update(delta_time)

    def on_draw(self):
        self.clear()
