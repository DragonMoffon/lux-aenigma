from weakref import proxy, ProxyType
from lux.systems.base import System, _ComponentSource

from lux.components import LevelObject, Player
from lux.components.player import PlayerState

from util.uuid_ref import UUIDRef


class PlayerInputSystem(System):
    requires = frozenset((Player,))

    update_priority: int = 0  # This is so manual like damn -.-, maybe a config file instead?

class PlayerStateSystem(System):
    requires = frozenset((Player,))

    update_priority: int = 1  # This is so manual like damn -.-, maybe a config file instead?

    def __init__(self):
        super().__init__()

        self.player_data: ProxyType[Player] = None
        self.player_object: UUIDRef[LevelObject] = None

    def preload(self):
        self.player_data: ProxyType[Player] = None
        self.player_object: UUIDRef[LevelObject] = None


    def load(self, source: _ComponentSource):
        player_data = source.get_components(Player)

        if len(player_data) > 1:
            raise ValueError("A level should not contain more than one player")

        self.player_data = proxy(player_data.pop())
        self.player_object = self.player_data.parent

    def update(self, dt: float):
        """
        ??? Is this really the best way to do this
        """

        self.player_data.state = PlayerState.IDLE

        if self.player_data.velcoity:
            if self.player_data.is_grabbing and self.player_data.grabbed_control_point is not None:
                self.player_data.state = PlayerState.PULLING
            elif self.player_data.is_crouching:
                self.player_data.state = PlayerState.CRAWLING
            else:
                self.player_data.state = PlayerState.MOVING
        else:
            if self.player_data.is_grabbing and self.player_data.grabbed_control_point is not None:
                self.player_data.state = PlayerState.GRABBING
            elif self.player_data.is_crouching:
                self.player_data.state = PlayerState.CROUCHING

