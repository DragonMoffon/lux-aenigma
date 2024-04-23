from math import tau

from arcade.draw_commands import draw_line_strip, draw_point
from arcade.window_commands import get_window
from pyglet.math import Vec2

from lux.engine.player.player_object import PlayerData
from lux.util.procedural_animator import ProceduralAnimator

OFFSET = 6.0
RADIUS = 16.0

LOCUS_COUNT = 2
LOCUS_POS_FREQ = 3.0
LOCUS_POS_DAMP = 0.5
LOCUS_POS_RESP = 2.0

BUBBLE_COUNT = 16
BUBBLE_WIDTH = 6


def get_locus_sdf(origin: Vec2, locus: Vec2, radius: float) -> Vec2:
    diff = (origin - locus)
    length = diff.mag - radius
    x, y = diff.normalize()
    return Vec2(x * length, y * length)


def smin(a: Vec2, b: Vec2, k) -> Vec2:
    # A smoothing function which uses a cubic polynomial similar to smooth-step

    # We want 6x the distance we start smoothing at.
    k *= 6.0

    # Pull the x and y values out because Vec2 operations are slow
    a_x, a_y = a.x, a.y
    b_x, b_y = b.x, b.y

    h_x = max(k - abs(a_x - b_x), 0.0) / k
    h_y = max(k - abs(a_y - b_y), 0.0) / k

    x = min(a_x, b_x) - h_x * h_x * h_x * k * (1.0 / 6.0)
    y = min(a_y, b_y) - h_y * h_y * h_y * k * (1.0 / 6.0)

    return Vec2(x, y)


class SDFBubble:

    def __init__(self, p: Vec2, c: Vec2, a: Vec2):
        self._primary_locus: Vec2 = p
        self._primary_radius: float = RADIUS
        self._control_locus: Vec2 = c
        self._control_radius: float = RADIUS
        self._anim_locus: Vec2 = a
        self._anim_radius: float = RADIUS

        self._primary_smoothing: float = 0.0
        self._secondary_smoothing: float = 0.0

        self._points: tuple[Vec2, ...] = tuple(Vec2.from_polar(1.0, tau * idx/BUBBLE_COUNT) for idx in range(BUBBLE_COUNT))

    def draw(self, colour):
        draw_line_strip(self._points + (self._points[0],), colour, BUBBLE_WIDTH)

    def get_sdf(self, origin: Vec2) -> Vec2:
        primary = get_locus_sdf(origin, self._primary_locus, self._primary_radius)
        control = get_locus_sdf(origin, self._control_locus, self._control_radius)
        anim = get_locus_sdf(origin, self._anim_locus, self._anim_radius)

        return smin(smin(primary, control, self._primary_smoothing), anim, self._secondary_smoothing)


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
        # self.triangles = tuple((a - locus, b - locus) for a, b in zip(self.points[0:-1], self.points[1:]))

    def update(self, dt, locus, direction):
        self.points = tuple(p.update(dt, locus, direction) for p in self.bubble_points)
        # self.triangles = tuple((a - locus, b - locus) for a, b in zip(self.points[0:-1], self.points[1:]))

    def draw(self, colour):
        draw_line_strip(self.points + (self.points[0],), colour, BUBBLE_WIDTH)


class PlayerRenderer:
    def __init__(self, player: PlayerData):
        self._ctx = get_window().ctx

        self._player: PlayerData = player

        self.locus_a: Vec2 = Vec2()
        self.locus_da: Vec2 = Vec2()
        self.locus_b: Vec2 = Vec2()

        self.locus_animator = ProceduralAnimator(
            LOCUS_POS_FREQ, LOCUS_POS_DAMP, LOCUS_POS_RESP,
            self.locus_a, self.locus_b, Vec2()
        )

        self.bubble = Bubble(self.locus_a)

    def update(self, delta_time: float):
        new_a = self._player.origin

        self.locus_da = (new_a - self.locus_a)

        self.locus_a = new_a
        self.locus_b = self.locus_animator.update(delta_time, new_a, self.locus_da)

        self.bubble.update(delta_time, self.locus_a, self._player.velocity.normalize())

    def draw(self):
        self._ctx.point_size = 6

        c = self._player.colour.to_int_color()
        self.bubble.draw(c)
