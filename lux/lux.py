import importlib.resources as pkg_resources

import arcade
from arcade import Window

import lux.data.fonts
from lux.views.mainmenu import MenuView

FPS_CAP = 240


with pkg_resources.path(lux.data.fonts, "gohu.ttf") as p:
    arcade.text.load_font(str(p))


class LuxGame(Window):
    def __init__(self):
        super().__init__(1280, 720, update_rate = 1 / FPS_CAP, title = "Lux Aenigma")

        self.show_view(MenuView())


def main():
    LuxGame().run()


if __name__ == "__main__":
    main()
