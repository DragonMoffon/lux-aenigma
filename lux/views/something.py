from pyglet.math import Vec2

from lux.engine.debug.ray_renderer import BeamDebugRenderer
from lux.util.view import LuxView
from lux.util.maths import Direction
from lux.engine.colour import LuxColour
from lux.engine.lights.ray import Ray
from lux.engine.lights.beam_light_ray import BeamLightRay
from lux.engine.interactors.interactor_edge import RayInteractorEdge
from lux.engine.interactors.filter import FilterRayInteractor
from lux.engine.debug import DebugRenderer
from lux.engine.debug.ray_interactor_renderer import RayInteractorRenderer


class SomethingView(LuxView):

    def __init__(self, back: LuxView):
        super().__init__(back=back)

        w, h = self.window.width / 2, self.window.height / 2

        self.renderer = DebugRenderer()

        beam = BeamLightRay(
            LuxColour.WHITE(),
            Ray(Vec2(w, h + 150.0), Direction.EAST(), 2500.0, 2500.0),
            Ray(Vec2(w, h - 150.0), Direction.EAST(), 2500.0, 2500.0)
        )

        self.filter_red = FilterRayInteractor(Vec2(w+125, h+50), Direction.WEST(), LuxColour.RED(), (RayInteractorEdge(Vec2(0.0, -50.0), Vec2(0.0, 50.0), True),))
        self.filter_green = FilterRayInteractor(Vec2(w+400, h+25), Direction.NORTHEAST(), LuxColour.GREEN(), (RayInteractorEdge(Vec2(0.0, -50.0), Vec2(0.0, 50.0), True),))
        self.filter_blue = FilterRayInteractor(Vec2(w+200, h-75), Direction.SOUTHWEST(), LuxColour.BLUE(), (RayInteractorEdge(Vec2(0.0, -50.0), Vec2(0.0, 50.0), True),))
        self.filter_cyan = FilterRayInteractor(Vec2(w+200, h-100), Direction.SOUTHWEST(), LuxColour.CYAN(), (RayInteractorEdge(Vec2(0.0, -50.0), Vec2(0.0, 50.0), False),))

        self.renderer.append(RayInteractorRenderer(self.filter_red))
        self.renderer.append(RayInteractorRenderer(self.filter_green))
        self.renderer.append(RayInteractorRenderer(self.filter_blue))
        self.renderer.append(RayInteractorRenderer(self.filter_cyan))

        self.edge_map = {
            self.filter_red.bounds[0].adjust(self.filter_red.origin, self.filter_red.direction.heading): self.filter_red,
            self.filter_green.bounds[0].adjust(self.filter_green.origin, self.filter_green.direction.heading): self.filter_green,
            self.filter_blue.bounds[0].adjust(self.filter_blue.origin, self.filter_blue.direction.heading): self.filter_blue,
            self.filter_cyan.bounds[0].adjust(self.filter_cyan.origin, self.filter_cyan.direction.heading): self.filter_cyan,
        }

        beams = beam.propagate_ray(self.edge_map)
        for beam in beams:
            self.renderer.append(BeamDebugRenderer(beam))

    def on_draw(self):
        self.clear()
        self.renderer.draw()
