from array import array
from random import random
from math import pi, cos, sin

from arcade.math import lerp_2d
from arcade.gl import BufferDescription
from arcade.window_commands import get_window
from pyglet.math import Vec2

from lux.engine.player.player_object import PlayerData
from lux.engine.colour import LuxColour

from arcade import draw_line

from lux.util.shader import get_shader

OFFSET = 6.0
RADIUS = 6.0
PLAYER_SPEED = 10.0


class PlayerRenderer:

    def __init__(self, player: PlayerData):
        self._ctx = get_window().ctx

        self._player: PlayerData = player

        self.locus_a: Vec2 = Vec2()
        self.locus_b: Vec2 = Vec2()

        self.orbit_points_a_1 = None
        self.orbit_points_a_2 = None

        self.points_program = self._ctx.program(
            vertex_shader = get_shader("points_vertex"),
            fragment_shader = get_shader("points_fragment"),
        )

        # TODO: Add random bursts of velocity. Also is it really worth doing this on the GPU?
        # The main argument for it is the fact that we can keep it all on the GPU it is not
        # the stripes actually mean anything beyond personalization.
        self.orbit_program = self._ctx.program(
            vertex_shader = get_shader("orbit_vertex")
        )

        self.orbit_program["consts"] = (0.1, 100.0, 1000000.0, 1.0)  # Min, Max, Gravity, Decay
        self.orbit_program["count"] = 6  # There are 6 points per locus.

        # Make two buffers we transform between, so we can work on the previous result
        self.buffer_1 = self._ctx.buffer(data=array('f', (self._gen_initial())))
        self.buffer_2 = self._ctx.buffer(reserve=self.buffer_1.size)

        # We also need to be able to visualize both versions (draw to the screen)
        self.vao_1 = self._ctx.geometry([BufferDescription(self.buffer_1, '2f 2x4', ['in_pos'])])
        self.vao_2 = self._ctx.geometry([BufferDescription(self.buffer_2, '2f 2x4', ['in_pos'])])

        # We need to be able to transform both buffers (ping-pong)
        self.gravity_1 = self._ctx.geometry([BufferDescription(self.buffer_1, '2f 2f', ['in_pos', 'in_vel'])])
        self.gravity_2 = self._ctx.geometry([BufferDescription(self.buffer_2, '2f 2f', ['in_pos', 'in_vel'])])

    def _gen_initial(self):
        for _ in range(12):
            theta = 2.0 * pi * random()
            x, y = cos(theta), sin(theta)
            # Position
            yield x * RADIUS
            yield y * RADIUS
            # Velocity
            yield -y * RADIUS
            yield x * RADIUS

    def update(self, delta_time: float):
        self.locus_a = self._player.origin
        self.locus_b = Vec2(*lerp_2d(self.locus_b, self.locus_a, delta_time * PLAYER_SPEED))

        self.orbit_program["dt"] = delta_time
        self.orbit_program["locus"] = (self.locus_a.x, self.locus_a.y, self.locus_b.x, self.locus_b.y)

        self.gravity_1.transform(self.orbit_program, self.buffer_2)
        self.gravity_1, self.gravity_2 = self.gravity_2, self.gravity_1
        self.vao_1, self.vao_2 = self.vao_2, self.vao_1
        self.buffer_1, self.buffer_2 = self.buffer_2, self.buffer_1

        print(array('f', self.buffer_1.read()))

    def draw(self):
        self._ctx.point_size = 6
        self.vao_1.render(self.points_program, mode=self._ctx.POINTS)

        c = LuxColour.RED.to_int_color()
        o = self.locus_a
        draw_line(
            o.x - OFFSET, o.y - OFFSET,
            o.x + OFFSET, o.y + OFFSET,
            c,
            2.0
        )
        draw_line(
            o.x + OFFSET, o.y - OFFSET,
            o.x - OFFSET, o.y + OFFSET,
            c,
            2.0
        )
        o = self.locus_b
        draw_line(
            o.x - OFFSET, o.y - OFFSET,
            o.x + OFFSET, o.y + OFFSET,
            c,
            2.0
        )
        draw_line(
            o.x + OFFSET, o.y - OFFSET,
            o.x - OFFSET, o.y + OFFSET,
            c,
            2.0
        )
