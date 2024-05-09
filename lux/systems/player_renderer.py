from math import tau

from weakref import proxy, ProxyType

from pyglet import shapes
from lux.get_window import get_window

from util.procedural_animator import ProceduralAnimator

from lux.systems.base import System, _ComponentSource
from lux.components.player import Player, LevelObject
from util.uuid_ref import UUIDRef

from lux.util.duration_tracker import perf_timed_context
from pyglet.math import Vec2

from logging import getLogger

logger = getLogger("lux")

OFFSET = 6.0
RADIUS = 16.0

LOCUS_COUNT = 2
LOCUS_POS_FREQ = 3.0
LOCUS_POS_DAMP = 0.5
LOCUS_POS_RESP = 2.0

BUBBLE_COUNT = 16
BUBBLE_WIDTH = 6

NORMAL_TEST = 0.0001


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
        self._batch = shapes.Batch()
        self._triangle_indices = tuple((0, i, (i+1)%BUBBLE_COUNT) for i in range(1, BUBBLE_COUNT))
        self._triangles = tuple(shapes.Triangle(*self.points[a], *self.points[b], *self.points[c], batch=self._batch) for a,b,c in self._triangle_indices)

    def update(self, dt, locus, direction):
        self.points = tuple(p.update(dt, locus, direction) for p in self.bubble_points)

    def draw(self, colour):
        for idx in range(len(self._triangle_indices)):
            triangle = self._triangles[idx]
            if triangle.color != colour:
                triangle.color = colour

            a, b, c = self._triangle_indices[idx]
            triangle.x, triangle.y = self.points[a]
            triangle.x2, triangle.y2 = self.points[b]
            triangle.x3, triangle.y3 = self.points[c]
        self._batch.draw()


class PlayerRenderer(System):
    requires = frozenset((Player,))

    update_priority: int = 3
    draw_priority: int = 0

    def __init__(self):
        super().__init__()
        self._ctx = get_window().ctx

        self._player_data: ProxyType[Player] = None
        self._player_object: UUIDRef[LevelObject] = None

        self.locus_a: Vec2 = None
        self.locus_da: Vec2 = None
        self.locus_b: Vec2 = None

        self.locus_animator = None

        self.bubble = None

    def preload(self):
        self._player_data: ProxyType[Player] = None
        self._player_object: UUIDRef[LevelObject] = None

        self.locus_a: Vec2 = Vec2()
        self.locus_da: Vec2 = Vec2()
        self.locus_b: Vec2 = Vec2()

        self.locus_animator = ProceduralAnimator(
            LOCUS_POS_FREQ, LOCUS_POS_DAMP, LOCUS_POS_RESP,
            self.locus_a, self.locus_b, Vec2()
        )

        self.bubble = Bubble(self.locus_a)

    def load(self, source: _ComponentSource):
        player_data = source.get_components(Player)

        if len(player_data) > 1:
            raise ValueError("A level should not contain more than one player")

        self._player_data = proxy(tuple(player_data)[0])
        self._player_object = self._player_data.parent

    def unload(self):
        self._player_data: ProxyType[Player] = None
        self._player_object: UUIDRef[LevelObject] = None

        self.locus_a: Vec2 = None
        self.locus_da: Vec2 = None
        self.locus_b: Vec2 = None

        self.locus_animator = None

        self.bubble = None

    @perf_timed_context()
    def update(self, dt: float):
        new_a = self._player_object.origin

        self.locus_da = (new_a - self.locus_a)

        self.locus_a = new_a
        self.locus_b = self.locus_animator.update(dt, new_a, self.locus_da)

        self.bubble.update(dt, self.locus_a, self._player_data.velocity.normalize())

    @perf_timed_context()
    def draw(self):
        c = self._player_object.colour.to_int_color()
        self.bubble.draw(c)