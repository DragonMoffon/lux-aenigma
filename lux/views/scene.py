
from pyglet.math import Vec2

from lux.util.view import LuxView
from lux.util.maths import Direction
from lux.engine.colour import LuxColour
from lux.engine.lights.ray import BeamLightRay, Ray


class SceneView(LuxView):

    def __init__(self, back: LuxView):
        super().__init__(back=back)

        self.beam = BeamLightRay(
            Vec2(self.window.width / 2, self.window.height / 2),
            Direction.EAST(),
            250.0,
            LuxColour.WHITE(),
            Ray(),
            Ray()
        )

    def on_draw(self):
        self.clear()
