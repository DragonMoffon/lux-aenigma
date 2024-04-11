from lux.engine.level.level_object import LevelObject

from lux.engine.player.player_object import PlayerData
from lux.engine.player.player_controller import PlayerController
from lux.engine.player.player_renderer import PlayerRenderer


class Level:
    """
    A single level which is equal to one "puzzle", but can be split into multiple sections.
    """
    def __init__(self, objects: set[LevelObject] = None, renderer: set = None, debug: set = None, player: PlayerData = None):
        self._player: PlayerData = player or PlayerData()
        self._player_controller: PlayerController = PlayerController(self._player)
        self._player_renderer: PlayerRenderer = PlayerRenderer(self._player)

        self._objects: set[LevelObject] = objects or {self._player}
        self._object_renderers: set = renderer or {self._player_renderer}
        self._object_debug_renderers: set = debug or set()

    def add_object(self, new_object: LevelObject):
        self._objects.add(new_object)

    def remove_object(self, old_object: LevelObject):
        self._objects.discard(old_object)

    def draw_level(self):
        for renderer in self._object_renderers:
            renderer.draw()

    def on_update(self, delta_time: float):
        self._player_controller.update(delta_time)
        self._player_renderer.update(delta_time)

    def debug_draw_level(self):
        for renderer in self._object_debug_renderers:
            renderer.draw()
