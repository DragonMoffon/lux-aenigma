from typing import TypedDict

from lux.util.view import LuxView

from lux.engine.level.level import Level
from lux.engine.player.player_object import PlayerData
from lux.engine.debug.debug_renderer import DebugRenderer
from lux.engine.debug.player_renderer import PlayerDebugRenderer

from pyglet.math import Vec2
from lux.engine.colour import LuxColour


class PlayerTestView(LuxView):

    def __init__(self, back: LuxView):
        super().__init__(back=back)
        self.debug_renderer = DebugRenderer()
        self.player_object: PlayerData = PlayerData(LuxColour.WHITE, Vec2(0.0, 0.0), Vec2(1.0, 0.0))

        self.debug_renderer.append(PlayerDebugRenderer(self.player_object))

        self.test_level: Level = Level(
            objects={self.player_object},
            debug={self.debug_renderer},
            player=self.player_object
        )

    def on_update(self, delta_time: float):
        self.test_level.on_update(delta_time)

    def on_draw(self):
        self.clear()
        self.test_level.debug_draw_level()
