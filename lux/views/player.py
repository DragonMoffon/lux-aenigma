import arcade.key
from arcade import Text
from pyglet.math import Vec2

from lux.engine.colour import LuxColour
from lux.engine.debug.debug_renderer import DebugRenderer
from lux.engine.debug.player_renderer import PlayerDebugRenderer
from lux.engine.level.level import Level
from lux.engine.player.player_object import PlayerData, PlayerConsts
from lux.engine.level.level_object import DebugLevelObject
from lux.engine.control_points.control_point import ControlPoint
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
        self.debug_control_point: ControlPoint = ControlPoint(self.debug_object, Vec2(10.0, 10.0), LuxColour.GREEN)

        self.debug_renderer.append(PlayerDebugRenderer(self.player_object))
        self.debug_renderer.append(BaseChildRenderer(self.debug_object))
        self.debug_renderer.append(ControlPointRenderer(self.debug_control_point))

        self.test_level: Level = Level(
            objects={self.player_object},
            debug={self.debug_renderer},
            player=self.player_object
        )

        self.mouse_look = False
        self._mouse_debug = (0.0, 0.0)
        self.mouse_label = Text(f"MOUSE: {self.mouse_look}", 5, self.window.height - 5, anchor_y = "top")

    def on_update(self, delta_time: float):
        self.test_level.on_update(delta_time)

        self.player_object.grabbed_control_point = None
        dist = self.debug_control_point.test_grab(self.player_object.origin, self.player_object.colour)
        if dist <= PlayerConsts.GRAB_RADIUS:
            self.player_object.grabbed_control_point = self.debug_control_point

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            self.mouse_look = not self.mouse_look
            self.mouse_label.text = f"MOUSE: {self.mouse_look}"
        return super().on_key_press(symbol, modifiers)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        if self.mouse_look:
            self.player_object.origin = Vec2(x, y)
            self.player_object.direction = Direction(dx, dy)
            self._mouse_debug = (dx, dy)

    def on_draw(self):
        self.clear()
        self.test_level.draw_level()
        self.test_level.debug_draw_level()
        self.mouse_label.draw()
