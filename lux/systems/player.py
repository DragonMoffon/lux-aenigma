from weakref import proxy, ProxyType

from arcade.experimental.input import InputManager, ActionState
from pyglet.math import Vec2

from lux.get_window import get_window
from lux.systems.base import System, _ComponentSource

from lux.components import LevelObject, Player
from lux.components.player import PlayerState

from util.uuid_ref import UUIDRef

from lux.consts import CONSTS


class PlayerInputSystem(System):
    requires = frozenset((Player,))

    update_priority: int = 0  # This is so manual like damn -.-, maybe a config file instead?

    def __init__(self):
        super().__init__()
        self._player_data: ProxyType[Player] = None
        self._player_object: UUIDRef[LevelObject] = None

        self._input_manager: InputManager = None

    def preload(self):
        self._player_data: ProxyType[Player] = None
        self._player_object: UUIDRef[LevelObject] = None

        self._input_manager: InputManager = get_window().input_manager

    def load(self, source: _ComponentSource):
        player_data = source.get_components(Player)

        if len(player_data) > 1:
            raise ValueError("A level should not contain more than one player")

        self._player_data = proxy(tuple(player_data)[0])
        self._player_object = self._player_data.parent

        self._input_manager.subscribe_to_action('player_crouch', self.set_is_crouching)
        self._input_manager.subscribe_to_action('player_grab', self.set_is_grabbing)

    def unload(self):
        self._player_data: ProxyType[Player] = None
        self._player_object: UUIDRef[LevelObject] = None

        self._input_manager.action_subscribers['player_crouch'].discard(self.set_is_crouching)
        self._input_manager.action_subscribers['player_grab'].discard(self.set_is_grabbing)

    def set_is_crouching(self, state):
        match state:
            case ActionState.PRESSED:
                self._player_data.is_crouching = True
            case ActionState.RELEASED:
                self._player_data.is_crouching = False

    def set_is_grabbing(self, state):
        match state:
            case ActionState.PRESSED:
                self._player_data.is_grabbing = True
            case ActionState.RELEASED:
                self._player_data.is_grabbing = False

    def update(self, dt: float):
        player_move_dir = Vec2(self._input_manager.axis("player_h"), self._input_manager.axis("player_v")).normalize()

        self._player_data.velocity = player_move_dir * CONSTS['PLAYER_SPEED'] * (1.0 - 0.6 * self._player_data.is_crouching)
        self._player_object.origin += self._player_data.velocity * dt
        self._player_object.direction = player_move_dir


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

        self.player_data = proxy(tuple(player_data)[0])
        self.player_object = self.player_data.parent

    def update(self, dt: float):
        """
        ??? Is this really the best way to do this
        """

        self.player_data.state = PlayerState.IDLING

        if self.player_data.velocity.dot(self.player_data.velocity) > 0.0:
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

