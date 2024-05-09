import arcade
import pyglet

from util.procedural_animator import ProceduralAnimator

from lux.util.view import LuxView
from lux.views.level import LevelView
from lux.data import get_sfx

from lux.level import LevelLoader

# Use Something Like the dev menu to list all levels (to test the level config works)
# Based on the procedurally animated thing I did for arcade-experiments

class LevelTestView(LuxView):

    def __init__(self, back: LuxView):
        super().__init__(back=back)

        self._level_loader = LevelLoader()
        self._level_loader.load_level_names()
        self._packs = {
            "test": self._level_loader.test_levels,
            "story": self._level_loader.story_levels,
            "challenges": self._level_loader.challenge_levels,
            "user": self._level_loader.user_levels
        }
        self._packs.update(self._level_loader.packs)
        self._pack_names = tuple(self._packs.keys())

        self._level_view: LevelView = LevelView(self, self._level_loader)

        self._levels = ()

        self._is_selecting_level: bool = False
        self.pack_selected = 0
        self.level_selected = 0

        self._move_sound = get_sfx('blip_c')
        self._pack_sound = get_sfx('blip_e')
        self._level_sound = get_sfx('blip_a')
        self._pack_animator: ProceduralAnimator = ProceduralAnimator(1.0, 0.75, 1.0, 0.0, 0.0, 0.0)
        self._level_animator: ProceduralAnimator = ProceduralAnimator(1.0, 0.5, 2.0, 0.0, 0.0, 0.0)

        self._gui_cam: arcade.camera.Camera2D = arcade.camera.Camera2D()
        self._pack_cam: arcade.camera.Camera2D = arcade.camera.Camera2D(position=(0.0, 0.0), viewport=(10, 10, self.window.width//2-20, self.window.height-100))
        self._pack_cam.equalise()
        self._level_cam: arcade.camera.Camera2D = arcade.camera.Camera2D(position=(0.0, 0.0), viewport=(self.window.width//2 + 10, 10, self.window.width//2-20, self.window.height-100))
        self._level_cam.equalise()

        self._pack_batch = pyglet.shapes.Batch()
        self._pack_text = []
        text_start = 0
        max_right = float("inf")
        for level_pack in self._pack_names:
            t = arcade.Text(level_pack, 0, text_start, font_name="GohuFont 11 Nerd Font Mono", font_size=22, batch=self._pack_batch, anchor_x="center", anchor_y="center")
            self._pack_text.append(t)
            text_start = t.bottom - 10
            max_right = min(t.right, max_right)

        self._level_batch = pyglet.shapes.Batch()
        self._level_text = []

        self._pack_selector_left = arcade.Text(">", int(max_right) - 10, 0, font_name="GohuFont 11 Nerd Font Mono", font_size=22, batch=self._pack_batch, anchor_x="right", anchor_y="center")
        self._pack_selector_right = arcade.Text("<", 10 - int(max_right), 0, font_name="GohuFont 11 Nerd Font Mono", font_size=22, batch=self._pack_batch, anchor_x="left", anchor_y="center")

        self._level_selector_left = arcade.Text(">", int(max_right) - 10, 0, font_name="GohuFont 11 Nerd Font Mono", font_size=22, batch=self._level_batch, anchor_x="right", anchor_y="center")
        self._level_selector_right = arcade.Text("<", 10 - int(max_right), 0, font_name="GohuFont 11 Nerd Font Mono", font_size=22, batch=self._level_batch, anchor_x="left", anchor_y="center")

        self._pack_header = arcade.Text("Level Packs", int(0.25 * self.window.width), self.window.height-10, font_name="GohuFont 11 Nerd Font Mono", font_size=40, anchor_x="center", anchor_y="top")
        self._level_header = arcade.Text("Levels", int(0.75 * self.window.width), self.window.height-10, font_name="GohuFont 11 Nerd Font Mono", font_size=40, anchor_x="center", anchor_y="top")

        self.calc_level_text()

    def calc_level_text(self):
        pack = self._pack_names[self.pack_selected]
        self._levels = self._packs[pack]

        self._level_text = []

        if not self._levels:
            return

        text_start = 0
        max_right = float("inf")
        for level in self._levels:
            t = arcade.Text(level, 0, text_start, font_name="GohuFont 11 Nerd Font Mono", font_size=22, batch=self._level_batch, anchor_x="center", anchor_y="center")
            self._level_text.append(t)
            text_start = t.bottom - 10
            max_right = min(t.right, max_right)

        self._level_selector_left = arcade.Text(">", int(max_right) - 10, 0, font_name="GohuFont 11 Nerd Font Mono", font_size=22, batch=self._level_batch, anchor_x="right", anchor_y="center")
        self._level_selector_right = arcade.Text("<", 10 - int(max_right), 0, font_name="GohuFont 11 Nerd Font Mono", font_size=22, batch=self._level_batch, anchor_x="left", anchor_y="center")

    def close(self):
        self.close()

    def select_prev(self):
        if self._is_selecting_level:
            if not self._levels:
                return
            old = self.level_selected
            self.level_selected = (self.level_selected - 1) % len(self._levels)
            new = self.level_selected
            y = self._level_text[self.level_selected].y
            self._level_selector_left.y = y
            self._level_selector_right.y = y
        else:
            old = self.pack_selected
            self.pack_selected = (self.pack_selected - 1) % len(self._pack_names)
            new = self.pack_selected
            y = self._pack_text[self.pack_selected].y
            self._pack_selector_left.y = y
            self._pack_selector_right.y = y

            if old != new:
                self.level_selected = 0
                self.calc_level_text()

        if old == new:
            self._pack_sound.play()
        self._move_sound.play()

    def select_next(self):
        if self._is_selecting_level:
            if not self._levels:
                return
            old = self.level_selected
            self.level_selected = (self.level_selected + 1) % len(self._levels)
            new = self.level_selected
            y = self._level_text[self.level_selected].y
            self._level_selector_left.y = y
            self._level_selector_right.y = y
        else:
            old = self.pack_selected
            self.pack_selected = (self.pack_selected + 1) % len(self._pack_names)
            new = self.pack_selected
            y = self._pack_text[self.pack_selected].y
            self._pack_selector_left.y = y
            self._pack_selector_right.y = y

            if old != new:
                self.level_selected = 0
                self.calc_level_text()

        if old == new:
            self._pack_sound.play()
        self._move_sound.play()

    def toggle(self):
        if self._is_selecting_level:
            self._level_sound.play()
        else:
            self._pack_sound.play()

        self._is_selecting_level = not self._is_selecting_level

    def select(self):
        if self._is_selecting_level:
            self._level_loader.start_pack(self.level_selected)

            self.window.show_view(self._level_view)
        else:
            self.load_pack()

        self.toggle()

    def load_pack(self):
        current_pack = self._pack_names[self.pack_selected]
        match current_pack:
            case "test":
                self._level_loader.load_test_levels()
            case "story":
                self._level_loader.load_story_levels()
            case "challenges":
                self._level_loader.load_challenge_levels()
            case "user":
                self._level_loader.load_user_levels()
            case _:
                self._level_loader.load_level_pack(current_pack)

    # ----- LOOP FUNCTIONS -----

    def on_update(self, delta_time: float):
        pos = self._pack_text[self.pack_selected].y
        self._pack_animator.update(delta_time, pos)
        self._pack_cam.position = 0, int(self._pack_animator.y)

        if len(self._levels):
            pos = self._level_text[self.level_selected].y
            self._level_animator.update(delta_time, pos)
            self._level_cam.position = 0, int(self._level_animator.y)

    def on_draw(self):
        self.clear(viewport=self.window.viewport)
        self._gui_cam.use()
        self._level_header.draw()
        self._pack_header.draw()

        if self._is_selecting_level:
            arcade.draw_rectangle_filled(
                self._level_header.x, self._level_header.bottom - 5,
                self._level_header.content_width, 4,
                (255, 255, 255, 255)
            )
        else:
            arcade.draw_rectangle_filled(
                self._pack_header.x, self._pack_header.bottom - 5,
                self._pack_header.content_width, 4,
                (255, 255, 255, 255)
            )

        self._pack_cam.use()
        self._pack_batch.draw()

        if self._levels:
            self._level_cam.use()
            self._level_batch.draw()


    # ---- INPUT FUNCTIONS ----

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case arcade.key.UP:
                self.select_prev()
            case arcade.key.W:
                self.select_prev()
            case arcade.key.DOWN:
                self.select_next()
            case arcade.key.S:
                self.select_next()
            case arcade.key.D:
                self.toggle()
            case arcade.key.RIGHT:
                self.toggle()
            case arcade.key.A:
                self.toggle()
            case arcade.key.LEFT:
                self.toggle()
            case arcade.key.SPACE:
                self.select()
            case arcade.key.ENTER:
                self.select()

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        if scroll_y >= 1:
            self.select_prev()
        elif scroll_y <= -1:
            self.select_next()

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.select()
