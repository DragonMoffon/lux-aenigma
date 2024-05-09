from typing import TypedDict, Protocol

from arcade import Texture
from pyglet.math import Vec2

from lux.components.base import Component, Resolvable
from lux.components.core import LevelObject

from util.uuid_ref import UUIDRef

SpriteDict = TypedDict(
    'SpriteDict',
    {
        'UUID': int,
        'parent': int,
        'depth': float,
        'scale': float,
        'anchor': tuple[float, float],
        'source': str,
        'rect': tuple[int, int, int, int],
    }
)


class _TextureLoader(Protocol):

    def load_texture(self, source: str, rect: tuple[int, int, int, int]) -> Texture:
        ...


class TextureResolvable:

    def __init__(self, source: str, rect: tuple[int, int, int, int]):
        self.source: str = source
        self.rect: tuple[int, int, int, int] = rect
        self._texture: Texture = None

    @property
    def texture(self):
        if self._texture is None:
            raise ValueError("Texture has not been resolved yet")

        return self._texture

    def resolve(self, source: _TextureLoader):
        self._texture = source.load_texture(self.source, self.rect)


class Sprite(Component):

    def __init__(self, UUID: int, parent: UUIDRef[LevelObject], texture: TextureResolvable, depth: float, scale: float, anchor: Vec2):
        super().__init__(UUID)
        self.parent: UUIDRef[LevelObject] = parent
        self.texture: TextureResolvable = texture
        self.depth: float = depth
        self.scale: float = scale
        self.anchor: Vec2 = anchor

    def serialise(self) -> SpriteDict:
        return {
            'UUID': self.UUID,
            'parent': self.parent._val,
            'depth': self.depth,
            'scale': self.scale,
            'anchor': (self.anchor.x, self.anchor.y),
            'source': self.texture.source,
            'rect': self.texture.rect,
        }

    @classmethod
    def deserialise(cls, data: SpriteDict) -> tuple[Component, tuple[Resolvable, ...]]:
        anchor = Vec2(*data['anchor'])
        parent = UUIDRef(data['parent'])
        texture = TextureResolvable(data['source'], data['rect'])
        return cls(data['UUID'], parent, texture, data['depth'], data['scale'], anchor), (parent, texture)

