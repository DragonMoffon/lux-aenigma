from pyglet.math import Vec2

from arcade.experimental.input import InputManager, ActionState

from lux.get_window import get_window
from lux.engine.player.player_object import PlayerData

from lux.consts import CONSTS


class PlayerController:

    def __init__(self, player_object: PlayerData):
        self._player: PlayerData = player_object
        self.input_manager: InputManager = get_window().input_manager

        self.input_manager.subscribe_to_action("player_crouch", self.set_is_crouching)
        self.input_manager.subscribe_to_action("player_grab", self.set_is_grabbing)

    def set_is_crouching(self, state):
        match state:
            case ActionState.PRESSED:
                self._player.is_crouching = True
            case ActionState.RELEASED:
                self._player.is_crouching = False

    def set_is_grabbing(self, state):
        match state:
            case ActionState.PRESSED:
                self._player.is_grabbing = True
            case ActionState.RELEASED:
                self._player.is_grabbing = False

    def update(self, delta_time):
        player_move_dir = Vec2(self.input_manager.axis("player_h"), self.input_manager.axis("player_v")).normalize()

        self._player.velocity = player_move_dir * CONSTS['PLAYER_SPEED'] * (1.0 - 0.6 * self._player.is_crouching)
        self._player.origin += self._player.velocity * delta_time
        self._player.direction = player_move_dir
