from lux.lib.view import LuxView


class SceneView(LuxView):

    def __init__(self, back: LuxView):
        super().__init__(back=back)

    def on_draw(self):
        self.clear()
