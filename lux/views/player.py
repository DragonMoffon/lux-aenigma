import arcade.key
from arcade import Text
from pyglet.math import Vec2

from lux.util.colour import LuxColour
from lux.engine.debug.debug_renderer import DebugRenderer
from lux.engine.debug.player_renderer import PlayerDebugRenderer
from lux.engine.level.level import Level
from lux.engine.player.player_object import PlayerData, PlayerConsts
from lux.engine.level.level_object import DebugLevelObject
from lux.engine.control_points.control_point import ControlPoint
from lux.engine.control_points.dof import RotationDOF
from lux.util.view import LuxView
from lux.util.maths import Direction

from lux.engine.debug.control_point_renderer import ControlPointRenderer
from lux.engine.debug.debug_renderer import BaseChildRenderer


class PlayerTestView(LuxView):

    def __init__(self, back: LuxView):
        super().__init__(back=back)
        self.debug_renderer = DebugRenderer()
        self.player_object: PlayerData = PlayerData(LuxColour.WHITE, Vec2(0.0, 0.0), Vec2(1.0, 0.0))
        x, y = self.window.center
        self.debug_object: DebugLevelObject = DebugLevelObject(LuxColour.WHITE, Vec2(x, y), Vec2(1.0, 0.0))

        self._rotation_dof: RotationDOF = RotationDOF(self.debug_object)

        self.debug_control_point: ControlPoint = ControlPoint(self.debug_object, Vec2(15.0, 15.0), LuxColour.GREEN, dof=(self._rotation_dof,))

        self.debug_renderer.append(PlayerDebugRenderer(self.player_object))
        self.debug_renderer.append(BaseChildRenderer(self.debug_object))
        self.debug_renderer.append(ControlPointRenderer(self.debug_control_point))

        self.test_level: Level = Level(
            objects={self.player_object},
            debug={self.debug_renderer},
            player=self.player_object
        )

        self._mouse_debug = Vec2(0.0, 0.0)

    def on_update(self, delta_time: float):
        self.test_level.on_update(delta_time)
        if self.player_object.is_grabbing:
            self.debug_control_point.pull(self._mouse_debug, 100.0 * delta_time)

    def on_key_press(self, symbol: int, modifiers: int):
        return super().on_key_press(symbol, modifiers)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self._mouse_debug = Vec2(x, y)

    def on_draw(self):
        self.clear()
        self.test_level.draw_level()
        self.test_level.debug_draw_level()
