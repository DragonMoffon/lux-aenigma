import importlib.resources as pkg_resources

import arcade
from arcade import Texture, Sprite, SpriteList
from arcade.geometry import is_point_in_box
from arcade.experimental.bloom_filter import BloomFilter

from lux.util.colour import LuxColour
from lux.util.music_mixer import RGBMusicMixer
from lux.util.view import LuxView

import lux.data.music


class MusicMixerView(LuxView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sounds: list[arcade.Sound] = []
        for s in ["stem_1.mp3", "stem_2.mp3", "stem_3.mp3"]:
            with pkg_resources.path(lux.data.music, s) as p:
                sounds.append(arcade.load_sound(p))
        self.rgbmusic = RGBMusicMixer(sounds)

        self.red = (0, 0, 0, 0)
        self.green = (0, 0, 0, 0)
        self.blue = (0, 0, 0, 0)
        self.square = (0, 0, 0, 0)
        self.color_square = (0, 0, 0, 0)

        self.tex = Texture.create_empty("rgbmusic", (1280, 720))
        self.sprite = Sprite(self.tex, center_x=self.window.width // 2, center_y=self.window.height // 2)
        self.sprite_list = SpriteList()
        self.sprite_list.append(self.sprite)

        self.bloom_level = 5.0
        self.bloom_filter = BloomFilter(1280, 720, 5.0)

        self.calc_pos()

    def on_show_view(self):
        super().on_show_view()
        self.rgbmusic.play()
        self.bloom_level = 5.0
        self.bloom_filter = BloomFilter(1280, 720, 5.0)

    def on_hide_view(self):
        super().on_hide_view()
        self.rgbmusic.pause()
        self.rgbmusic.seek(0)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if is_point_in_box((self.red[0], self.red[2]), (x, y), (self.red[1], self.red[3])):
                self.rgbmusic.red = not self.rgbmusic.red
                self.dirty = True
            elif is_point_in_box((self.green[0], self.green[2]), (x, y), (self.green[1], self.green[3])):
                self.rgbmusic.green = not self.rgbmusic.green
                self.dirty = True
            elif is_point_in_box((self.blue[0], self.blue[2]), (x, y), (self.blue[1], self.blue[3])):
                self.rgbmusic.blue = not self.rgbmusic.blue
                self.dirty = True

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.bloom_level += 1.0
            self.bloom_filter = BloomFilter(1280, 720, self.bloom_level)
        elif symbol == arcade.key.DOWN:
            self.bloom_level -= 1.0
            self.bloom_filter = BloomFilter(1280, 720, self.bloom_level)
        self.dirty = True
        return super().on_key_press(symbol, modifiers)

    def calc_pos(self):
        ww, wh = arcade.get_window().size
        wcw = ww / 2

        one_third_h = wh / 3
        two_thirds_h = one_third_h * 2
        one_sixth_h = one_third_h / 2
        one_ninth_h = one_third_h / 3

        square_left = wcw - one_sixth_h
        square_center_x = wcw

        red_top = two_thirds_h
        red_bottom = green_top = red_top - one_ninth_h
        green_bottom = blue_top = green_top - one_ninth_h
        blue_bottom = blue_top - one_ninth_h

        ww, wh = arcade.get_window().size
        wcw = ww / 2

        one_third_h = wh / 3
        two_thirds_h = one_third_h * 2
        one_sixth_h = one_third_h / 2

        square_left = wcw - one_sixth_h
        square_center_x = wcw
        square_right = wcw + one_sixth_h
        square_top = two_thirds_h
        square_bottom = one_third_h

        self.red = (square_left, square_center_x, red_bottom, red_top)
        self.green = (square_left, square_center_x, green_bottom, green_top)
        self.blue = (square_left, square_center_x, blue_bottom, blue_top)
        self.square = (square_left, square_right, square_bottom, square_top)
        self.color_square = (square_center_x, square_right, square_bottom, square_top)

    def rerender(self):
        with arcade.get_window().ctx.default_atlas.render_into(self.tex) as fbo:
            fbo.clear()

            # Outline
            arcade.draw_lrbt_rectangle_outline(*self.square, arcade.color.GRAY, 5)

            # Lights
            if self.rgbmusic.red:
                arcade.draw_lrbt_rectangle_filled(*self.red, arcade.color.RED)
            if self.rgbmusic.green:
                arcade.draw_lrbt_rectangle_filled(*self.green, arcade.color.GREEN)
            if self.rgbmusic.blue:
                arcade.draw_lrbt_rectangle_filled(*self.blue, arcade.color.BLUE)

            # Color
            if self.rgbmusic.color != LuxColour.BLACK:
                arcade.draw_lrbt_rectangle_filled(*self.color_square, self.rgbmusic.color.to_int_color())

        # BLOOM
        self.bloom_filter.use()
        self.bloom_filter.clear()
        self.sprite_list.draw()

        self.window.use()
        self.clear()
        self.bloom_filter.draw()
        # Draw the original on top of the bloom because it looks better
        self.sprite_list.draw()
        return super().on_draw()
