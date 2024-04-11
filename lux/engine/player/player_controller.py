from pyglet.math import Vec2

from lux.engine.input import InputManager, ActionState

from lux.engine.input.inputs import Keys
from lux.engine.player.player_object import PlayerData


PLAYER_SPEED = 800.0


class PlayerController:

    def __init__(self, player_object: PlayerData):
        self._player: PlayerData = player_object
        self.input_manager: InputManager = InputManager()

        self.input_manager.new_action("crouch")
        self.input_manager.subscribe_to_action("crouch", self.set_is_crouching)
        self.input_manager.add_action_input("crouch", Keys.LSHIFT)

        self.input_manager.new_axis("h")
        self.input_manager.add_axis_input("h", Keys.D, scale=1.0)
        self.input_manager.add_axis_input("h", Keys.A, scale=-1.0)

        self.input_manager.new_axis("v")
        self.input_manager.add_axis_input("v", Keys.W, scale=1.0)
        self.input_manager.add_axis_input("v", Keys.S, scale=-1.0)

        self._is_crouching: bool = False

    def set_is_crouching(self, state):
        match state:
            case ActionState.PRESSED:
                self._is_crouching = True
            case ActionState.RELEASED:
                self._is_crouching = False

    def update(self, delta_time):
        self.input_manager.update()

        player_move_dir = Vec2(self.input_manager.axis("h"), self.input_manager.axis("v")).normalize()

        self._player.origin += player_move_dir * delta_time * PLAYER_SPEED * (1.0 - 0.6 * self._is_crouching)
        self._player.direction = player_move_dir
