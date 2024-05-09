import arcade

from weakref import WeakSet

from lux.systems.base import System, _ComponentSource

from lux.components import Sprite, LevelObject


class SpriteRenderer(System):
    requires = frozenset((Sprite,))
    draw_priority: int = 0

    def __init__(self):
        super().__init__()
        self._sprite_list: arcade.SpriteList = None
        self._sprite_data: WeakSet[Sprite] = None

        self._sprite_map: dict[int, arcade.Sprite] = None

    def preload(self):
        self._sprite_list = arcade.SpriteList()
        self._sprite_data = None
        self._sprite_map = {}

    def load(self, source: _ComponentSource):
        self._sprite_data = source.get_components(Sprite)

        for sprite in self._sprite_data:
            arcade_sprite = arcade.Sprite()
            sprite.add_listeners(('depth', 'scale', 'anchor_point'), self.update_sprite)
            sprite.parent.add_listeners(('origin', 'direction', 'colour'), self.update_level_object)
            self._sprite_map[sprite.UUID] = arcade_sprite
            self._sprite_map[sprite.parent.UUID] = arcade_sprite

            arcade_sprite.position = sprite.parent.origin
            arcade_sprite.radians = sprite.parent.direction.heading
            arcade_sprite.scale_xy = sprite.scale, sprite.scale
            arcade_sprite.texture = sprite.texture.texture
            arcade_sprite.depth = sprite.depth
            arcade_sprite.color = sprite.parent.colour.to_int_color()

            self._sprite_list.append(arcade_sprite)

    def update_sprite(self, sprite: Sprite, *args):
        pass

    def update_level_object(self, level_object: LevelObject, *args):
        pass

    def unload(self):
        if self._sprite_data is None:
            return

        for sprite in self._sprite_data:
            sprite.remove_listeners(('depth', 'scale', 'anchor_point'), self.update_sprite)
            sprite.parent.remove_listeners(('origin', 'direction', 'colour'), self.update_level_object)

        self._sprite_list.clear(deep=True)
        self._sprite_data = None
        self._sprite_map = None

    def draw(self):
        self._sprite_list.draw()