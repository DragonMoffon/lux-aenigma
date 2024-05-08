from lux.systems.base import System
from lux.components import LevelObject

class DebugRenderer(System):
    requires = frozenset((LevelObject,))
