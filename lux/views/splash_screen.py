from typing import NamedTuple, Generator
from math import sin, pi

from arcade import View, Sprite, load_texture
from lux.util.view import LuxView


class Splash(NamedTuple):
    src: str
    scale: float
    duration: float
    is_growing: bool
    is_pixelated: bool = True
    do_fade_in: bool = True
    do_fade_out: bool = True


SPLASHES = (
    Splash(
        ":textures:splashes/arcade-logo-splash.png",
        1.0,
        6.0,
        True,
        False
    ),
    Splash(
        ":textures:splashes/dragon-bakery-splash.png",
        1.0,
        6.0,
        False
    ),
    Splash(
        ":textures:splashes/DDHQ.png",
        0.1,
        6.0,
        False,
        False
    )
)


class SplashView(View):

    def __init__(self, next_view: type):
        super().__init__()
        self._next = next_view

        self._splash_sprite: Sprite = None
        self._splash_timer: float = 0.0
        self._current_splash: Splash = None
        self._splashes: Generator[Splash] = (splash for splash in SPLASHES)

    def _next_splash(self):
        self._current_splash = next(self._splashes, None)

        if self._current_splash is None:
            self._splash_sprite = None
            self.window.show_view(self._next())
            return

        self._splash_timer = 0.0

        self._splash_sprite.scale = self._current_splash.scale
        self._splash_sprite.texture = load_texture(self._current_splash.src)
        self._splash_sprite.scale = self._current_splash.scale
        self._splash_sprite.alpha = 255 * (not self._current_splash.do_fade_in)

    def on_show(self):
        self._splash_sprite = Sprite()
        self._next_splash()

    def on_update(self, delta_time: float):
        if self._current_splash is None:
            return

        self._splash_timer += delta_time

        if self._splash_timer >= self._current_splash.duration:
            self._next_splash()
            return

        self._splash_sprite.position = self.window.center

        splash_fraction = self._splash_timer / self._current_splash.duration

        if self._current_splash.is_growing:
            self._splash_sprite.scale = self._current_splash.scale + splash_fraction * 0.25

        fade_fraction = min(0.5 + 0.5 * self._current_splash.do_fade_out, max(0.5 - 0.5 * self._current_splash.do_fade_in, splash_fraction))
        self._splash_sprite.alpha = int(255 * sin(pi * fade_fraction))

    def on_draw(self):
        self.clear()

        if self._current_splash is None:
            return

        self._splash_sprite.draw(pixelated=self._current_splash.is_pixelated)
