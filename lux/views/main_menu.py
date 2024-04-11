import logging

from arcade import key

from lux.util.dev_menu import DevMenu
from lux.util.view import LuxView
from lux.views.musicmixer import MusicMixerView
from lux.views.scene import SceneView
from lux.views.editor import SceneEditorView
from lux.views.scene_select import SceneSelectView
from lux.views.fast_test import FastTestView
from lux.views.player import PlayerTestView

logger = logging.getLogger("lux")


class MenuView(LuxView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu = DevMenu({
            "Test": FastTestView(back = self),
            "Player": PlayerTestView(back = self),
            # "Scene": SceneView(back = self),
            # "Editor": SceneEditorView(back = self),
            # "Scene Select": SceneSelectView(back = self),
            "Music Mixer": MusicMixerView(back = self)
        })

    def on_key_press(self, symbol: int, modifiers: int):
        match symbol:
            case key.UP:
                self.menu.selected -= 1
            case key.DOWN:
                self.menu.selected += 1
            case key.ENTER:
                self.window.show_view(self.menu.current_view)

    def on_draw(self):
        self.clear()
        self.menu.draw()
