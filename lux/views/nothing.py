from lux.lib.view import LuxView


class NothingView(LuxView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_draw(self):
        self.clear()
