from weakref import WeakSet
from typing import TypedDict

from lux.components.base import Component
from lux.data import get_config, get_level_data, save_level_data
from lux.systems.base import System, UpdateLoopSystem, DrawLoopSystem

# This is so cursed, but it is a built-in safety for debugging -.- human error and all that.
import sys


PackConfigDict = TypedDict(
    "PackConfigDict",
    {
        'name': str,
        'levels': list[str]
    }
)

LevelConfigDict = TypedDict(
    "LevelConfigDict",
    {
        'test': list[str],
        'story': list[str],
        'challenges': list[str],
        'user': list[str],
        'packs': list[PackConfigDict]
    }
)


class LevelLoader:

    def __init__(self):
        self.all_levels: set[str] = set()
        self.test_levels: tuple[str, ...] = ()
        self.story_levels: tuple[str, ...] = ()
        self.challenge_levels: tuple[str, ...] = ()
        self.user_levels: tuple[str, ...] = ()
        self.packs: dict[str, tuple[str, ...]] = dict()

    def load_level_names(self):
        level_config: LevelConfigDict = get_config('levels').unwrap()

        # We use a set because we don't want duplicates.
        self.all_levels: set[str] = set()

        self.test_levels: tuple[str, ...] = tuple(level_config['test'])
        self.all_levels.update(self.test_levels)

        self.story_levels: tuple[str, ...] = tuple(level_config['story'])
        self.all_levels.update(self.story_levels)

        self.challenge_levels: tuple[str, ...] = tuple(level_config['challenges'])
        self.all_levels.update(self.challenge_levels)

        self.user_levels: tuple[str, ...] = tuple(level_config['user'])
        self.all_levels.update(self.user_levels)

        self.packs: dict[str, tuple[str, ...]] = dict()
        for pack in level_config.get('packs', ()):
            if pack['name'] in self.packs:
                raise ValueError("Two level packs have the same name")  # Should probably get caught
            levels = tuple(pack['levels'])
            self.all_levels.update(levels)
            self.packs[pack['name']] = levels

class Level:

    def __init__(self):
        self._raw_data: dict = None
        self._name: str = None

        # Only this parent Level object should hold strong refs to a component or system
        self.UUID_map: dict[int, Component] = None
        self.systems: tuple[System, ...] = None

        # These are helper storages used to quickly retrieve items
        self.component_map: dict[type[Component], WeakSet[Component]] = None
        self.update_systems: tuple[UpdateLoopSystem, ...] = None  # Currently unsorted, but may give systems a sorting value eventually.
        self.rendering_systems: tuple[DrawLoopSystem, ...] = None  # Currently unsorted, but may give systems a sorting value eventually.

    def preload(self, data: dict):
        """
        Create the systems required for the particular level,
        but don't create any components or initialise non-thread safe systems
        """
        pass

    def load(self):
        """
        Load the components of the system and initialised any systems still partially initialised.
        """
        pass

    def update(self, dt: float):
        for system in self.update_systems:
            system.update(dt)

    def draw(self):
        for system in self.rendering_systems:
            system.draw()

    def get_components_of_name(self, component: type[Component]) -> WeakSet[Component]:
        # Digi I am so sorry ;-;
        assert component in sys._getframe(1).f_locals[sys._getframe(1).f_code.co_varnames[0]].requires, "System is getting a set of components it doesn't say it requires"
        return self.component_map.get(component, WeakSet())

    def resolve_UUID(self, UUID_: int):
        if self.UUID_map is None:
            raise ValueError("Level has not been initialised yet")
        return self.UUID_map[UUID_]
