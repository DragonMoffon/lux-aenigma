import arcade
import arcade.easing as easing

from lux.util.view import LuxView

from lux.level import LevelLoader, Level

from lux.consts import CONSTS


# This is temporary. We need a good system for switching levels which we just don't have right now.
class LevelView(LuxView):

    def __init__(self, back: LuxView, level_loader: LevelLoader):
        super().__init__(back=back)

        self._level_loader: LevelLoader = level_loader
        self._current_level: Level = None
        self._transitioning_level: bool = False
        self._transition_time: float = 0.0
        self._level_cam: arcade.camera.Camera2D = arcade.camera.Camera2D(position=(0.0, 0.0))

        self._blackout_sprite: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self.window.width, self.window.height,
            color=(0, 0, 0, 255)
        )
        self._level_text: arcade.Text = arcade.Text("", 0, 0, font_name="GohuFont 11 Nerd Font Mono", font_size=22, anchor_x="center", anchor_y="center")

    def on_key_press(self, symbol: int, modifiers: int):
        if self._transitioning_level:
            self.end_transition()
            return
        elif symbol == arcade.key.ENTER:
            self._level_loader.load_next_level()
            self._current_level = self._level_loader.current_level

            if self._current_level is None:
                self.go_back()
                return

            self.start_transition()
            return

        super().on_key_press(symbol, modifiers)

    def on_hide_view(self):
        if self._current_level is not None:
            self._current_level.unload()

    def on_show_view(self):
        self._current_level = self._level_loader.current_level
        self.start_transition()

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self._level_cam.match_screen(and_projection=True)
        self._blackout_sprite.width = width
        self._blackout_sprite.height = height

    def start_transition(self):
        if self._current_level is None:
            return

        self._transition_time = 0.0
        self._transitioning_level = True
        self._blackout_sprite.width = self.window.width
        self._blackout_sprite.height = self.window.height
        self._blackout_sprite.alpha = 255
        self._level_text.text = self._current_level.name

    def end_transition(self):
        self._transitioning_level = False
        self._blackout_sprite.alpha = 0

    def on_update(self, delta_time: float):
        if self._transitioning_level:
            self._transition_time += delta_time
            p = self._transition_time / CONSTS["LEVEL_TRANSITION_SPEED"]
            if p >= 1.0:
                self.end_transition()

            alpha = int(255 * easing.ease_in_out_sin(1 - p))

            self._blackout_sprite.alpha = alpha
            self._level_text.color = (255, 255, 255, alpha)
        if self._current_level:
            self._current_level.update(delta_time)

    def on_draw(self):
        self.clear()
        self._level_cam.use()
        if self._current_level:
            self._current_level.draw()

        if self._transitioning_level:
            self._blackout_sprite.draw()
            self._level_text.draw()
