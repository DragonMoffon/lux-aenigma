from lux.components.base import Component

from lux.components.core import LevelObject
from lux.components.control import ControlPoint
from lux.components.player import Player
from lux.components.sprite import Sprite

__all__ = (
    'get_component_map',
    'Component',
    'LevelObject',
    'ControlPoint',
    'Player',
    'Sprite'
)

def get_component_map() -> dict[str, type[Component]]:
    return {
        component.__name__: component for component in Component.__subclasses__()
    }
