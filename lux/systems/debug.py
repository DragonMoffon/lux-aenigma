from math import degrees

from lux.systems.base import System, _ComponentSource
from lux.components import LevelObject

from weakref import WeakKeyDictionary, WeakSet
from arcade import SpriteList, SpriteCircle, SpriteSolidColor, BasicSprite

from lux.util import LuxColour
from lux.consts import CONSTS

from pyglet.math import Vec2


class DebugRenderer(System):
    requires = frozenset((LevelObject,))

    draw_priority: int = 1000

    def __init__(self):
        super().__init__()
        self._sprite_list: SpriteList = None
        self._component_core_map: WeakKeyDictionary[LevelObject, BasicSprite] = None
        self._component_direction_map: WeakKeyDictionary[LevelObject, BasicSprite] = None

    def preload(self):
        self._sprite_list: SpriteList = None
        self._component_core_map: WeakKeyDictionary[LevelObject, BasicSprite] = None
        self._component_direction_map: WeakKeyDictionary[LevelObject, BasicSprite] = None

    def load(self, source: _ComponentSource):
        self._sprite_list: SpriteList = SpriteList()
        self._component_core_map: WeakKeyDictionary[LevelObject, BasicSprite] = WeakKeyDictionary()
        self._component_direction_map: WeakKeyDictionary[LevelObject, BasicSprite] = WeakKeyDictionary()

        level_objects: WeakSet[LevelObject] = source.get_components(LevelObject)
        for obj in level_objects:
            core_sprite = SpriteCircle(
                CONSTS['DEBUG_POINT_RADIUS'],
                obj.colour.to_int_color()
            )
            core_sprite.position = obj.origin
            direction_sprite = SpriteSolidColor(CONSTS['DEBUG_POINT_RADIUS']*2, 2, color=(255, 125, 200, 255))
            direction_sprite.angle = degrees(obj.direction.heading)
            direction_sprite.position = obj.origin + obj.direction * CONSTS['DEBUG_POINT_RADIUS']

            self._sprite_list.extend((direction_sprite, core_sprite))

            self._component_core_map[obj] = core_sprite
            self._component_direction_map[obj] = direction_sprite

            obj.add_listener('origin', self.update_origin)
            obj.add_listener('direction', self.update_direction)
            obj.add_listener('colour', self.update_colour)

    def unload(self):
        if self._component_core_map is None:
            return

        for obj in self._component_core_map:
            obj.remove_listener('origin', self.update_origin)
            obj.remove_listener('direction', self.update_direction)
            obj.remove_listener('colour', self.update_colour)

        self._component_core_map = None
        self._component_direction_map = None
        self._sprite_list.clear(deep=True)

    def update_origin(self, component: LevelObject, attr: str, value: Vec2):
        self._component_core_map[component].position = value
        self._component_direction_map[component].position = value + component.direction * CONSTS['DEBUG_POINT_RADIUS']

    def update_direction(self, component: LevelObject, attr: str, value: Vec2):
        direction = self._component_direction_map[component]
        direction.position = component.origin + value * CONSTS['DEBUG_POINT_RADIUS']
        direction.angle = degrees(value.heading)

    def update_colour(self, component: LevelObject, attr: str, value: LuxColour):
        self._component_core_map[component].color = value.to_int_color()

    def draw(self):
        self._sprite_list.draw(pixelated=True)
