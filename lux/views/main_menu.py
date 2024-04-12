import logging

from arcade import key

from lux.util.dev_menu import DevMenu
from lux.util.view import LuxView
from lux.views.musicmixer import MusicMixerView
from lux.views.scene import SceneView
from lux.views.editor import SceneEditorView
from lux.views.scene_select import SceneSelectView
from lux.views.tri_test import TriTestView
from lux.views.fast_test import FastTestView
from lux.views.player import PlayerTestView
from lux.views.sevensegtest import SevenSegTestView

from time import time

logger = logging.getLogger("lux")


class MenuView(LuxView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        t = time()
        test = FastTestView(back = self)
        print(f"test: {time() - t}s")

        t = time()
        player = PlayerTestView(back = self)
        print(f"player: {time() - t}s")

        t = time()
        tri = TriTestView(back = self)
        print(f"triangle: {time() - t}s")

        t = time()
        mus = MusicMixerView(back = self)
        print(f"music: {time() - t}s")

        t = time()
        seven = SevenSegTestView(back = self)
        print(f"seven seg: {time() - t}s")

        self.menu = DevMenu({
            "Test": test,
            "Player": player,
            "Triangle": tri,
            # "Scene": SceneView(back = self),
            # "Editor": SceneEditorView(back = self),
            # "Scene Select": SceneSelectView(back = self),
            "Music Mixer": mus,
            "Seven Segment Display": seven
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
