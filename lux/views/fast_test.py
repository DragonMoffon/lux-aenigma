from logging import getLogger
# import timeit

import arcade
from pyglet.math import Vec2

from lux.engine.interactors import FilterRayInteractor, PortalRayInteractor, MirrorRayInteractor
from lux.engine.new import propogate_beam
from lux.util.view import LuxView
from lux.util.maths import Direction
from lux.engine.colour import LuxColour
from lux.engine.lights.ray import Ray
from lux.engine.lights.beam_light_ray import BeamLightRay
from lux.engine.interactors import RayInteractorEdge
from lux.engine.debug import DebugRenderer
from lux.engine.debug.ray_interactor_renderer import RayInteractorRenderer
from lux.engine.debug.light_renderer import BeamDebugRenderer

logger = getLogger("lux")


ONE_FRAME = 1/600
BEAM_LENGTH = 3500.0


class FastTestView(LuxView):

    def __init__(self, back: LuxView):
        super().__init__(back=back)
        w, h = self.window.center
        ww, wh = self.window.size

        self.renderer = DebugRenderer()

        self.offset = Vec2(0.0, 15.0)
        self.cen = Vec2(w, h)
        self.beam = BeamLightRay(
            LuxColour.WHITE,
            Ray(self.cen + self.offset.rotate(0.0), Direction.EAST.rotate(0.0), 3500.0, 3500.0),
            Ray(self.cen - self.offset.rotate(0.0), Direction.EAST.rotate(0.0), 3500.0, 3500.0)
        )
        self.t = 0.0

        # self.box_mirror_up = MirrorRayInteractor(ww, Vec2(ww/2.0, wh), Direction.SOUTH, LuxColour.WHITE)
        # self.box_mirror_lf = MirrorRayInteractor(wh, Vec2(0.0, wh/2.0), Direction.EAST, LuxColour.WHITE)
        # self.box_mirror_rt = MirrorRayInteractor(wh, Vec2(ww, wh/2.0), Direction.WEST, LuxColour.WHITE)
        # self.box_mirror_dw = MirrorRayInteractor(ww, Vec2(ww/2.0, 0), Direction.NORTH, LuxColour.WHITE)

        self.filter_red = FilterRayInteractor(Vec2(w+125, h+75), Direction.NORTHWEST, LuxColour.RED, (RayInteractorEdge(Vec2(0.0, -50.0), Vec2(0.0, 50.0), True),))
        self.mirror_green = MirrorRayInteractor(400, Vec2(w+400, h+25), Direction.SOUTHWEST, LuxColour.GREEN)
        self.mirror_blue = MirrorRayInteractor(100, Vec2(w+200, h-75), Direction.WEST, LuxColour.BLUE)
        self.filter_cyan_a = FilterRayInteractor(Vec2(w+100, h-35), Direction.NORTHWEST, LuxColour.CYAN, (RayInteractorEdge(Vec2(0.0, -25.0), Vec2(0.0, 25.0), False),))
        self.filter_cyan_b = FilterRayInteractor(Vec2(w+150, h-125), Direction.EAST, LuxColour.CYAN, (RayInteractorEdge(Vec2(0.0, -50.0), Vec2(0.0, 50.0), False),))
        self.portal_a, self.portal_b = PortalRayInteractor.create_pair(100, LuxColour.WHITE, Vec2(w+250, h), Direction.WEST, Vec2(w-100, h-50), Direction.EAST)

        self.interactors = (self.filter_cyan_a, self.filter_cyan_b, self.filter_red,
                            self.mirror_blue, self.mirror_green,
                            self.portal_a, self.portal_b)

        self.rerender()
        # t = (timeit(lambda: find_intersections(self.interactors, self.beam), number=10000) / 10000)
        # print(1 / t)
        # print(1 / t / 60)

        self.rev = False
        self.paused = False

        self.speed = 0.01
        self.turbo = False

    def rerender(self):
        self.renderer.clear()

        for interactor in self.interactors:
            self.renderer.append(RayInteractorRenderer(interactor))

        beams = propogate_beam(self.interactors, self.beam)

        def add_beam(beam):
            self.renderer.append(BeamDebugRenderer(beam))
            for child in beam.children:
                add_beam(child)
        for beam in beams:
            add_beam(beam)

    def shift_beam(self, delta_time: float):
        self.t += delta_time * self.speed * (-1 if self.rev else 1.0) * (10 if self.turbo else 1)

        angle = (self.t % 1.0) * 2.0 * 3.1415926
        self.beam = BeamLightRay(
            LuxColour.WHITE,
            Ray(self.cen + self.offset.rotate(angle), Direction.EAST.rotate(angle), BEAM_LENGTH, BEAM_LENGTH),
            Ray(self.cen - self.offset.rotate(angle), Direction.EAST.rotate(angle), BEAM_LENGTH, BEAM_LENGTH)
        )

        self.rerender()

    def on_update(self, delta_time: float):
        # return
        if self.paused:
            return

        self.shift_beam(delta_time)

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case arcade.key.ENTER:
                self.rev = not self.rev
            case arcade.key.SPACE:
                self.paused = not self.paused
                if self.paused:
                    self.rerender()
            case arcade.key.UP:
                self.t += ONE_FRAME
                if self.paused:
                    self.shift_beam(1/60)
            case arcade.key.DOWN:
                self.t -= ONE_FRAME
                if self.paused:
                    self.shift_beam(1/60)
            case arcade.key.NUM_MULTIPLY:
                self.turbo = True
            case arcade.key.NUM_0 | arcade.key.KEY_0:
                self.t = 0
                if self.paused:
                    self.shift_beam(0.0)

    def on_key_release(self, symbol: int, modifiers: int):
        match symbol:
            case arcade.key.NUM_MULTIPLY:
                self.turbo = False

    def on_draw(self):
        self.clear()
        self.renderer.draw()
