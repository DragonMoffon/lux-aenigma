from pyglet.math import Vec2

from lux.engine.debug.light_renderer import BeamDebugRenderer
from lux.util.view import LuxView
from lux.util.maths import Direction
from lux.engine.colour import LuxColour
from lux.engine.lights.ray import Ray
from lux.engine.lights.beam_light_ray import BeamLightRay
from lux.engine.interactors.interactor_edge import RayInteractorEdge
from lux.engine.interactors.filter import FilterRayInteractor
from lux.engine.debug import DebugRenderer
from lux.engine.debug.ray_interactor_renderer import RayInteractorRenderer

from math import pi


class SomethingView(LuxView):

    def __init__(self, back: LuxView):
        super().__init__(back=back)
        w, h = self.window.center

        self.renderer = DebugRenderer()

        self.beam = BeamLightRay(
            LuxColour.WHITE(),
            Ray(Vec2(w, h + 150.0), Direction.EAST(), 2500.0, 2500.0),
            Ray(Vec2(w, h - 150.0), Direction.EAST(), 2500.0, 2500.0)
        )
        self.beam_renderer = BeamDebugRenderer(self.beam)
        self.renderer.append(self.beam_renderer)
        self.t = 0.0

        self.filter_red = FilterRayInteractor(Vec2(w+125, h+75), Direction.NORTHWEST(), LuxColour.RED(), (RayInteractorEdge(Vec2(0.0, -50.0), Vec2(0.0, 50.0), True),))
        self.filter_green = FilterRayInteractor(Vec2(w+400, h+25), Direction.WEST(), LuxColour.GREEN(), (RayInteractorEdge(Vec2(0.0, -50.0), Vec2(0.0, 50.0), True),))
        self.filter_blue = FilterRayInteractor(Vec2(w+200, h-75), Direction.WEST(), LuxColour.BLUE(), (RayInteractorEdge(Vec2(0.0, -50.0), Vec2(0.0, 50.0), True),))
        self.filter_cyan_a = FilterRayInteractor(Vec2(w+100, h-35), Direction.WEST(), LuxColour.CYAN(), (RayInteractorEdge(Vec2(0.0, -25.0), Vec2(0.0, 25.0), False),))
        self.filter_cyan_b = FilterRayInteractor(Vec2(w+150, h-105), Direction.WEST(), LuxColour.CYAN(), (RayInteractorEdge(Vec2(0.0, -25.0), Vec2(0.0, 25.0), False),))

        self.edge_map = {
            self.filter_red.bounds[0].adjust(self.filter_red.origin, self.filter_red.direction.heading): self.filter_red,
            self.filter_green.bounds[0].adjust(self.filter_green.origin, self.filter_green.direction.heading): self.filter_green,
            # self.filter_blue.bounds[0].adjust(self.filter_blue.origin, self.filter_blue.direction.heading): self.filter_blue,
            # self.filter_cyan_a.bounds[0].adjust(self.filter_cyan_a.origin, self.filter_cyan_a.direction.heading): self.filter_cyan_a,
            # self.filter_cyan_b.bounds[0].adjust(self.filter_cyan_b.origin, self.filter_cyan_b.direction.heading): self.filter_cyan_b,
        }

        self.rerender()

    def rerender(self):
        self.renderer.clear()

        self.renderer.append(RayInteractorRenderer(self.filter_red))
        self.renderer.append(RayInteractorRenderer(self.filter_green))
        # self.renderer.append(RayInteractorRenderer(self.filter_blue))
        # self.renderer.append(RayInteractorRenderer(self.filter_cyan_a))
        # self.renderer.append(RayInteractorRenderer(self.filter_cyan_b))
        # self.renderer.append(self.beam_renderer)

        def make_beam_renderers(beam):
            self.renderer.append(BeamDebugRenderer(beam))
            for child in beam.children:
                make_beam_renderers(child)

        beams = self.beam.propagate_ray(self.edge_map)
        for beam in beams:
            make_beam_renderers(beam)

    def on_show_view(self):
        self.t = 0.0

    def on_update(self, delta_time: float):
        w, h = self.window.center
        cen = Vec2(w, h)
        self.t += delta_time * 0.005
        angle = (self.t % 1.0) * 2.0 * pi

        pos_shift = Vec2(0.0, 150.0).rotate(angle)
        beam_dir = Direction.EAST().rotate(angle)

        self.beam = BeamLightRay(
            LuxColour.WHITE(),
            Ray(cen + pos_shift, beam_dir, 2500.0, 2500.0),
            Ray(cen - pos_shift, beam_dir, 2500.0, 2500.0)
        )

        self.beam_renderer.update_child(self.beam)
        self.rerender()

    def on_draw(self):
        self.clear()
        self.renderer.draw()
