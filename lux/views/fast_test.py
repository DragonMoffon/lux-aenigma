from logging import getLogger

import arcade
from arcade.camera import Camera2D
from arcade.experimental.bloom_filter import BloomFilter
from pyglet.math import Vec2

from lux.engine.interactors import FilterRayInteractor, PortalRayInteractor, MirrorRayInteractor
from lux.engine.new import propogate_beam
from lux.util.colour import LuxColour
from lux.engine.lights.ray import Ray
from lux.engine.lights.beam_light_ray import BeamLightRay
from lux.engine.interactors import RayInteractorEdge
from lux.engine.debug import DebugRenderer
from lux.engine.debug.ray_interactor_renderer import RayInteractorRenderer
from lux.engine.debug.light_renderer import BeamDebugRenderer
from lux.util.view import LuxView
from lux.util.maths import Direction

from lux.engine.control_points.control_point import ControlPoint
from lux.engine.control_points.dof import RotationDOF
from lux.engine.debug.control_point_renderer import ControlPointRenderer

logger = getLogger("lux")


ONE_FRAME = 1/600
BEAM_LENGTH = 3500.0


class FastTestView(LuxView):

    def __init__(self, back: LuxView):
        super().__init__(back=back)
        w, h = self.window.center
        ww, wh = self.window.size

        self.cam = Camera2D()
        self.renderer = DebugRenderer()
        self.beam_renderer = DebugRenderer()

        self.bloom = BloomFilter(self.window.width, self.window.height, 20.0)

        self.offset = Vec2(0.0, 15.0)
        self.cen = Vec2(w, h)
        self.beam = BeamLightRay(
            LuxColour.WHITE,
            Ray(self.cen + self.offset.rotate(0.0), Direction.EAST.rotate(0.0), 3500.0, 3500.0),
            Ray(self.cen - self.offset.rotate(0.0), Direction.EAST.rotate(0.0), 3500.0, 3500.0)
        )
        self.t = 0.0

        self.box_mirror_up = MirrorRayInteractor(ww, Vec2(ww/2.0, wh), Direction.SOUTH, LuxColour.WHITE)
        self.box_mirror_lf = MirrorRayInteractor(wh, Vec2(0.0, wh/2.0), Direction.EAST, LuxColour.WHITE)
        self.box_mirror_rt = MirrorRayInteractor(wh, Vec2(ww, wh/2.0), Direction.WEST, LuxColour.WHITE)
        self.box_mirror_dw = MirrorRayInteractor(ww, Vec2(ww/2.0, 0), Direction.NORTH, LuxColour.WHITE)

        self.filter_red = FilterRayInteractor(Vec2(w+125, h+75), Direction.NORTHWEST, LuxColour.RED, (RayInteractorEdge(Vec2(0.0, -50.0), Vec2(0.0, 50.0), True),))
        self.mirror_green = MirrorRayInteractor(400, Vec2(w+400, h+25), Direction.SOUTHWEST, LuxColour.GREEN)
        self.mirror_blue = MirrorRayInteractor(100, Vec2(w+200, h-75), Direction.WEST, LuxColour.BLUE)
        self.filter_cyan_a = FilterRayInteractor(Vec2(w+100, h-35), Direction.NORTHWEST, LuxColour.CYAN, (RayInteractorEdge(Vec2(0.0, -25.0), Vec2(0.0, 25.0), False),))
        self.filter_cyan_b = FilterRayInteractor(Vec2(w+150, h-125), Direction.EAST, LuxColour.CYAN, (RayInteractorEdge(Vec2(0.0, -50.0), Vec2(0.0, 50.0), False),))
        self.portal_a, self.portal_b = PortalRayInteractor.create_pair(100, LuxColour.WHITE, Vec2(w+250, h), Direction.WEST, Vec2(w-100, h-50), Direction.EAST)

        self.interactors = [self.filter_cyan_a, self.filter_cyan_b, self.filter_red,
                            self.mirror_blue, self.mirror_green,
                            self.portal_a, self.portal_b,
                            self.box_mirror_dw, self.box_mirror_lf, self.box_mirror_rt, self.box_mirror_up]

        for interactor in self.interactors:
            self.renderer.append(RayInteractorRenderer(interactor))

        self._rot_dof = RotationDOF(self.portal_a)
        self._control_point = ControlPoint(self.portal_a, Vec2(-15.0, 0.0), LuxColour.WHITE, (self._rot_dof,))
        self.renderer.append(ControlPointRenderer(self._control_point))

        self.rerender()
        # t = (timeit(lambda: find_intersections(self.interactors, self.beam), number=10000) / 10000)
        # print(1 / t)
        # print(1 / t / 60)

        self.rev = False
        self.paused = False
        self.bloom_toggle = True
        self.mirrors = False

        self.speed = 0.01
        self.turbo = False

        self._mouse_debug = Vec2(0.0, 0.0)

    def rerender(self):
        beams = propogate_beam(self.interactors, self.beam)

        self.beam_renderer.clear()

        def add_beam(beam):
            self.beam_renderer.append(BeamDebugRenderer(beam))
            for child in beam.children:
                add_beam(child)
        for beam in beams:
            add_beam(beam)

    def toggle_mirror_box(self):
        return

        # THIS DOES NOT WORK
        # YOU CAN'T REMOVE INTERACTORS MID GAME, IT BREAKS
        mirrors = [self.box_mirror_dw, self.box_mirror_lf, self.box_mirror_rt, self.box_mirror_up]

        if self.mirrors:
            self.interactors.extend(mirrors)
        else:
            [self.interactors.remove(m) for m in mirrors]

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
            self._control_point.pull(self._mouse_debug, 250.0 * delta_time)
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
            case arcade.key.M:
                self.mirrors = not self.mirrors
                self.toggle_mirror_box()
            case arcade.key.Z:
                self.cam.zoom = 0.5
            case arcade.key.B:
                self.bloom_toggle = not self.bloom_toggle

        super().on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int):
        match symbol:
            case arcade.key.NUM_MULTIPLY:
                self.turbo = False

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self._mouse_debug = Vec2(x, y)

    def on_draw(self):
        self.clear()

        if self.bloom_toggle:
            self.bloom.use()
            self.bloom.clear()
            self.beam_renderer.draw()

            self.window.use()
            self.bloom.draw()
            self.renderer.draw()
        else:
            self.window.use()
            self.beam_renderer.draw()
            self.renderer.draw()
