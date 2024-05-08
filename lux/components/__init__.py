from lux.components.base import Component

from lux.components.core import LevelObject
from lux.components.control import ControlPoint

def get_component_map() -> dict[str, type[Component]]:
    return {
        LevelObject.__name__: LevelObject,
        ControlPoint.__name__: ControlPoint
    }