from collections import deque
from arcade import Window, Text
from lux.views.main_menu import MenuView
from lux.views.splash_screen import SplashView

FPS_CAP = 24000
FPS_QUEUE = 10

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class LuxWindow(Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, update_rate = 1 / FPS_CAP, title = "Lux Aenigma")
        self.register_event_type("on_action")
        self.show_view(SplashView(MenuView))

        self._begun = False

        self.fps_queue = deque(maxlen = FPS_QUEUE)
        self.frame_count = 0

        self.fps_text = Text("???.? FPS", SCREEN_WIDTH - 5, SCREEN_HEIGHT - 5,
                             anchor_x="right", anchor_y = "top",
                             font_name="GohuFont 11 Nerd Font Mono", font_size = 11)

    def on_action(self, action: str, action_state):
        pass

    def on_update(self, delta_time: float):
        self.frame_count += 1
        self.fps_queue.append(1 / delta_time)
        if self.frame_count % FPS_QUEUE == 0:
            avg = sum(self.fps_queue) / FPS_QUEUE
            self.fps_text.text = f"{avg:.1f} FPS"
        return super().on_update(delta_time)

    def debug_draw(self):
        self.fps_text.draw()

    def on_draw(self):
        self.debug_draw()

