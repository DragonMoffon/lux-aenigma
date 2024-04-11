from random import random, choice
from math import pi, tau, cos, sin

from arcade.draw_commands import draw_line_strip
from arcade.window_commands import get_window
from pyglet.math import Vec2

from lux.engine.player.player_object import PlayerData
from lux.engine.colour import LuxColour
from lux.util.procedural_animator import ProceduralAnimator

from arcade import draw_line

OFFSET = 6.0
RADIUS = 16.0

LOCUS_COUNT = 2
LOCUS_POS_FREQ = 3.0
LOCUS_POS_DAMP = 0.5
LOCUS_POS_RESP = 2.0

BUBBLE_COUNT = 16

SCRIBBLE_LEN = 16
SCRIBBLE_WIDTH = 2
SCRIBBLE_MAX_T_OFFSET = 0.5
SCRIBBLE_MAX_T_VARIATION = 0.05
SCRIBBLE_BASE_T = 1.0/100.0
SCRIBBLE_COUNT = 4


class Scribble:

    def __init__(self, locuses):
        self.points = ()
        self.locus_idx = ()
        self._new_points()
        self.t = SCRIBBLE_MAX_T_OFFSET * random()
        self.trigger_t = SCRIBBLE_BASE_T + random() * SCRIBBLE_MAX_T_VARIATION

    def draw(self, colour, locuses):
        points = tuple(locuses[idx] + offset for idx, offset in zip(self.locus_idx, self.points))
        draw_line_strip(points, colour, SCRIBBLE_WIDTH)

    def _new_points(self):
        self.points = tuple(Vec2(RADIUS * random(), 0.0).rotate(2.0 * pi * random()) for _ in range(SCRIBBLE_LEN))
        self.locus_idx = tuple(choice((0, 0, 0, 0, 1)) for _ in range(SCRIBBLE_LEN))

    def update(self, dt):
        self.t += dt
        if self.t >= self.trigger_t:
            self.t -= self.trigger_t
            self._new_points()


class BubblePoint:

    def __init__(self, angle, locus):
        self.original_dir = Vec2.from_polar(1.0, angle)
        self.original_offset = self.original_dir * RADIUS
        pos = locus + self.original_offset

        self.animator = ProceduralAnimator(
            LOCUS_POS_FREQ, LOCUS_POS_DAMP, LOCUS_POS_RESP,
            pos, pos, Vec2()
        )

    def update(self, dt, new_locus, new_dir):
        target = new_locus + self.original_offset
        dot = new_dir.dot(self.original_dir)
        self.animator.update_values(new_frequency=3.0*(0.5*dot + 0.5) + 3.0, new_response=dot)

        return self.animator.update(dt, target)

    @property
    def pos(self):
        return self.animator.y


class Bubble:

    def __init__(self, locus):
        self.bubble_points = tuple(BubblePoint(tau * idx/BUBBLE_COUNT, locus) for idx in range(BUBBLE_COUNT))
        self.points = tuple(p.pos for p in self.bubble_points)
        self.triangles = tuple((a - locus, b - locus) for a, b in zip(self.points[0:-1], self.points[1:]))

    def update(self, dt, locus, direction):
        self.points = tuple(p.update(dt, locus, direction) for p in self.bubble_points)
        self.triangles = tuple((a - locus, b - locus) for a, b in zip(self.points[0:-1], self.points[1:]))

    def draw(self, colour):
        draw_line_strip(self.points, colour, SCRIBBLE_WIDTH)

    def get_scribble_points(self):
        for _ in range(SCRIBBLE_LEN):
            t_a, t_b = choice(self.triangles)
            r_a, r_b = random(), random()
            if r_a + r_b > 1.0:
                r_a, r_b = 1.0 - r_a, 1.0 - r_b

            yield t_a * r_a + t_b * r_b


class PlayerRenderer:

    def __init__(self, player: PlayerData):
        self._ctx = get_window().ctx

        self._player: PlayerData = player

        self.locus_a: Vec2 = Vec2()
        self.locus_da: Vec2 = Vec2()
        self.locus_b: Vec2 = Vec2()

        self.locus_animator: ProceduralAnimator = ProceduralAnimator(
            LOCUS_POS_FREQ, LOCUS_POS_DAMP, LOCUS_POS_RESP,
            self.locus_a, self.locus_b, Vec2()
        )

        # Find some way to get the scribble effect, but only have one draw_lines call.
        # It doesn't look as good with only one scribble it really requires at least 2
        # However just simply doing the for loop loses a load of frames.
        self.scribbles: tuple[Scribble, ...] = tuple(Scribble((self.locus_a, self.locus_b)) for _ in range(SCRIBBLE_COUNT))

        self.bubble = Bubble(self.locus_a)
        self.scribble_points_a = tuple(self.bubble.get_scribble_points())
        self.scribble_points_b = tuple(self.bubble.get_scribble_points())

        self.scribble_t_a = SCRIBBLE_MAX_T_OFFSET * random()
        self.scribble_t_b = SCRIBBLE_MAX_T_OFFSET * random()


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
        new_a = self._player.origin

        self.locus_da = (new_a - self.locus_a)

        self.locus_a = new_a
        self.locus_b = self.locus_animator.update(delta_time, new_a, self.locus_da)

        #for scribble in self.scribbles:
        #    scribble.update(delta_time)

        self.bubble.update(delta_time, self.locus_a, self._player.direction)
        self.scribble_t_a += delta_time
        if self.scribble_t_a >= SCRIBBLE_BASE_T:
            self.scribble_t_a -= SCRIBBLE_BASE_T
            self.scribble_points_a = tuple(self.bubble.get_scribble_points())

        self.scribble_t_b += delta_time
        if self.scribble_t_b >= SCRIBBLE_BASE_T:
            self.scribble_t_b -= SCRIBBLE_BASE_T
            self.scribble_points_b = tuple(self.bubble.get_scribble_points())

    def draw(self):
        self._ctx.point_size = 6

        c = self._player.colour.to_int_color()
        # for scribble in self.scribbles:
        #     scribble.draw(c, (self.locus_a, self.locus_b))

        if self.scribble_points_a:
            points = tuple(self.locus_a + p for p in self.scribble_points_a)
            draw_line_strip(points, c, SCRIBBLE_WIDTH)

        if self.scribble_points_b:
            points = tuple(self.locus_a + p for p in self.scribble_points_b)
            draw_line_strip(points, c, SCRIBBLE_WIDTH)

        # self.bubble.draw(c)

        c = LuxColour.RED.to_int_color()
        o = self.locus_a
        # draw_line(
        #     o.x - OFFSET, o.y - OFFSET,
        #     o.x + OFFSET, o.y + OFFSET,
        #     c,
        #     2.0
        # )
        # draw_line(
        #     o.x + OFFSET, o.y - OFFSET,
        #     o.x - OFFSET, o.y + OFFSET,
        #     c,
        #     2.0
        # )
        o = self.locus_b
        # draw_line(
        #     o.x - OFFSET, o.y - OFFSET,
        #     o.x + OFFSET, o.y + OFFSET,
        #     c,
        #     2.0
        # )
        # draw_line(
        #     o.x + OFFSET, o.y - OFFSET,
        #     o.x - OFFSET, o.y + OFFSET,
        #     c,
        #     2.0
        # )
