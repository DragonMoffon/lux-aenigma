from arcade.math import lerp_2d
from pyglet.math import Vec2

from lux.engine.player.player_object import PlayerData


class PlayerAnimator:

    def __init__(self, player: PlayerData):
        self._player: PlayerData = player

        self.locus_a: Vec2 = Vec2()
        self.locus_b: Vec2 = Vec2()

    def update(self, delta_time: float):
        self.locus_a = self._player.origin
        self.locus_b = lerp_2d(self.locus_b, self.locus_a, delta_time)
