import importlib.resources as pkg_resources

import arcade
import lux.data.fonts

from lux import get_window

FPS_CAP = 240

with pkg_resources.path(lux.data.fonts, "gohu.ttf") as p:
    arcade.text.load_font(str(p))


def main():
    get_window().run()


if __name__ == "__main__":
    main()
