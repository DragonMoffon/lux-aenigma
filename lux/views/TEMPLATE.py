from lux.util.view import LuxView


class REPLACEView(LuxView):

    def __init__(self, back: LuxView):
        super().__init__(back=back)

    def on_draw(self):
        self.clear()
