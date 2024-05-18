from lux.systems.base import System, UpdateLoopSystem, DrawLoopSystem
from lux.components import Component

from lux.systems.control import ControlPointSystem
from lux.systems.player import PlayerInputSystem, PlayerStateSystem
from lux.systems.player_renderer import PlayerRenderer
from lux.systems.debug import DebugRenderer
from lux.systems.sprite_renderer import SpriteRenderer


# Due to how get_system_requirement_map works we don't actually need to have any systems in this system, but eh.
__all__ = (
    'get_systems',
    'get_system_requirement_map',
    'ControlPointSystem',
    'PlayerInputSystem',
    'PlayerStateSystem',
    'PlayerRenderer',
    'SpriteRenderer',
    'DebugRenderer'
)


def get_systems() -> tuple[type[System], ...]:
    """
    Get the list of every system subclass. Due to how globals works this is just a list of every system
    imported here, but it is still less human input than manually defining the list.
    """
    return tuple(System.__subclasses__())


def get_system_requirement_map() -> dict[type[Component], tuple[type[System], ...]]:
    """
    AAAAAAAAAAHHHHHHHHHHHHHHHHHHHHHHHHHHHH
    """
    systems = get_systems()
    requirement_map: dict[type[Component], tuple[type[System], ...]] = dict()
    for system in systems:
        for component in system.requires:
            requirement_map[component] = requirement_map.get(component, ()) + (system,)

    return requirement_map
