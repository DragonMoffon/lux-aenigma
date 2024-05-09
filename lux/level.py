from weakref import WeakSet
from typing import TypedDict, TypeVar

from lux.components.base import Component
from lux.components import get_component_map
from lux.data import get_config, get_level_data
from lux.systems.base import System, UpdateLoopSystem, DrawLoopSystem
from lux.systems import get_system_requirement_map

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

LevelDataDict = TypedDict(
    "LevelDataDict",
    {
        "challenge_times": list[float, float, float],
        "bounds": list,
        "components": dict[str, list[dict]]
    }
)

C = TypeVar('C', bound=Component)


class Level:

    def __init__(self, name: str):
        self._name: str = name
        self._raw_data: LevelDataDict = None
        self._loaded: bool = False

        # Only this parent Level object should hold strong refs to a component or system
        self.UUID_map: dict[int, Component] = None
        self.systems: tuple[System, ...] = None

        # These are helper storages used to quickly retrieve items
        self.component_map: dict[type[Component], WeakSet[Component]] = None
        self.update_systems: tuple[UpdateLoopSystem, ...] = None
        self.draw_systems: tuple[DrawLoopSystem, ...] = None

    @property
    def name(self):
        return self._name

    @property
    def raw_data(self):
        return self._raw_data

    def preload(self, data: LevelDataDict):
        """
        Create the systems required for the particular level, but don't create any components
        """
        self._raw_data = data
        components = data['components']

        component_map = get_component_map()
        requirement_map = get_system_requirement_map()

        required_systems = set()
        for component_name in components:
            component_type = component_map[component_name]
            required_systems.update(requirement_map[component_type])

        self.systems = tuple(system() for system in required_systems)
        update_systems: list[UpdateLoopSystem] = []
        draw_systems: list[DrawLoopSystem] = []
        for system in self.systems:
            if hasattr(system, 'update'):
                update_systems.append(system)

            if hasattr(system, 'draw'):
                draw_systems.append(system)

            system.preload()

        self.update_systems = tuple(sorted(update_systems, key=lambda s: s.update_priority))
        self.draw_systems = tuple(sorted(draw_systems, key=lambda s: s.draw_priority))

    def load(self):
        """
        Load the components of the levels and finish initialising systems.
        """
        if self._raw_data is None:
            raise ValueError("Level has not be preloaded cannot load it yet")

        components = self._raw_data['components']
        component_map = get_component_map()

        self.UUID_map = dict()
        self.component_map = dict()

        all_resolvers = []

        for component_name in components:
            component_type = component_map[component_name]
            self.component_map[component_type] = WeakSet()
            for component_data in components[component_name]:
                component, resolvers = component_type.deserialise(component_data)
                all_resolvers.extend(resolvers)
                self.UUID_map[component.UUID] = component
                self.component_map[component_type].add(component)

        for resolver in all_resolvers:
            resolver.resolve(self)

        for system in self.systems:
            system.load(self)

        self._loaded = True

    def unload(self):
        """
        Unload all systems and delete the components
        """
        if self._raw_data is None:
            raise ValueError("Level has not be preloaded cannot load it yet")

        for system in self.systems:
            system.unload()

        self.component_map = None
        self.UUID_map = None

        self._loaded = False

    def update(self, dt: float):
        if not self._loaded:
            return

        for system in self.update_systems:
            system.update(dt)

    def draw(self):
        if not self._loaded:
            return

        for system in self.draw_systems:
            system.draw()

    def get_components(self, component: type[C]) -> WeakSet[C]:
        # Digi I am so sorry ;-;
        assert component in sys._getframe(1).f_locals[sys._getframe(1).f_code.co_varnames[0]].requires, "System is getting a set of components it doesn't say it requires"
        return self.component_map.get(component, WeakSet())

    def resolve_UUID(self, UUID_: int):
        if self.UUID_map is None:
            raise ValueError("Level has not been initialised yet")
        return self.UUID_map[UUID_]


class LevelLoader:

    def __init__(self):
        self.all_levels: set[str] = set()
        self.test_levels: tuple[str, ...] = ()
        self.story_levels: tuple[str, ...] = ()
        self.challenge_levels: tuple[str, ...] = ()
        self.user_levels: tuple[str, ...] = ()
        self.packs: dict[str, tuple[str, ...]] = dict()

        self.current_pack_name: str = None
        self.current_pack_index: int = None
        self.current_level: Level = None
        self.current_pack_level_names: tuple[str, ...] = None
        self.current_pack_levels: tuple[Level, ...] = None

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

    def load_pack(self, pack_name: str, pack_levels: tuple[str, ...]):
        # for now a level pack is just a name and list of level names, but eventually it should also store info
        # like whether it should auto move to the next level and whether is should show completion time between levels

        self.unload_pack()

        self.current_pack_name = pack_name
        self.current_pack_level_names = pack_levels

        _levels = []
        for level in pack_levels:
            try:
                data: LevelDataDict = get_level_data(level).unwrap()
            except FileNotFoundError:
                continue
            level_obj = Level(level)
            level_obj.preload(data)
            _levels.append(level_obj)

        self.current_pack_levels = tuple(_levels)

        self.current_pack_index = None
        self.current_level = None

    def start_pack(self, idx: int = 0):
        if self.current_pack_name is None:
            raise ValueError("No pack currently loaded")

        if len(self.current_pack_levels) <= idx:
            raise ValueError(f"Trying to get a level at an invalid index {idx}")

        self.current_pack_index = idx
        self.current_level = self.current_pack_levels[self.current_pack_index]

        self.load_current_level()

    def load_current_level(self):
        self.current_level.load()

    def unload_current_level(self):
        self.current_level.unload()

    def load_next_level(self):
        self.unload_current_level()
        self.current_pack_index += 1

        if self.current_pack_index < len(self.current_pack_levels):
            self.current_level = self.current_pack_levels[self.current_pack_index]
            self.load_current_level()
            return

        self.finish_pack()

    def finish_pack(self):
        # Depending on how the pack is configured what happens here changes, but for now it just unloads the pack,
        # and goes back to the level select screen
        self.unload_pack()

        # This is where I would use a notification because I don't want a direct connection between the Level view
        # and the LevelLoader, but for now the Level view just calls this when I press the back button

    def unload_pack(self):
        if self.current_pack_name is None:
            return

        for level in self.current_pack_levels:
            level.unload()

        self.current_pack_name = None
        self.current_pack_level_names = None
        self.current_pack_levels = None
        self.current_level = None
        self.current_pack_index = None

    # ---- PACK LOADING ----
    # -.- Hate this lmao

    def load_test_levels(self):
        self.load_pack("test", self.test_levels)

    def load_story_levels(self):
        self.load_pack("story", self.story_levels)

    def load_challenge_levels(self):
        self.load_pack("challenge", self.challenge_levels)

    def load_user_levels(self):
        self.load_pack("user", self.user_levels)

    def load_level_pack(self, name: str):
        pack = self.packs[name]
        self.load_pack(name, pack)
