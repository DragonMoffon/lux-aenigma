from arcade import Window
from lux.views.mainmenu import MenuView

FPS_CAP = 240


class LuxWindow(Window):

    def __init__(self):
        super().__init__(1280, 720, update_rate = 1 / FPS_CAP, title = "Lux Aenigma")
        self.show_view(MenuView())
