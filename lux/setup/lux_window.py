from collections import deque
from logging import getLogger

from arcade import Window, Text, get_controllers
from arcade.key import GRAVE
from arcade.experimental import input

from lux.views.main_menu import MenuView
from lux.views.splash_screen import SplashView
from lux.engine.debug.menu import DebugDisplay
from lux.data import get_config

logger = getLogger('lux')

FPS_CAP = 24000
FPS_QUEUE = 10

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


def action(*args):
    print(args)


class LuxWindow(Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, update_rate=1 / FPS_CAP, title="Lux Aenigma")
        self.register_event_type("on_action")

        self._input_manager: input.InputManager = input.InputManager.parse(get_config("active_input").unwrap())
        controllers = get_controllers()
        if controllers:
            self._input_manager.bind_controller(controllers[0])

        self.show_view(SplashView(MenuView))

        self._begun = False

        self.fps_queue = deque(maxlen=FPS_QUEUE)
        self.frame_count = 0

        self.fps_text = Text("???.? FPS", SCREEN_WIDTH - 5, SCREEN_HEIGHT - 5,
                             anchor_x="right", anchor_y="top",
                             font_name="GohuFont 11 Nerd Font Mono", font_size=11)

        self.debug_display = DebugDisplay(self)

    @property
    def input_manager(self) -> input.InputManager:
        return self._input_manager

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == GRAVE:
            self.debug_display.show = not self.debug_display.show

    def _dispatch_updates(self, delta_time: float):
        self._input_manager.update()

        # FPS tracking
        self.frame_count += 1
        self.fps_queue.append(1 / delta_time)
        if self.frame_count % FPS_QUEUE == 0:
            avg = sum(self.fps_queue) / FPS_QUEUE
            self.fps_text.text = f"{avg:.1f} FPS"

        # Dispatch on_update for window and views
        super()._dispatch_updates(delta_time)

    def debug_draw(self):
        with self.default_camera.activate():
            self.fps_text.draw()
            self.debug_display.draw()

    def on_draw(self):
        self.debug_draw()

