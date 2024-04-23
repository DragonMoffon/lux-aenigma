from pyglet.math import Vec2
from pyglet.input import get_controllers

from lux.engine.input import InputManager, ActionState

from lux.engine.input.inputs import Keys, ControllerAxes
from lux.engine.player.player_object import PlayerData


PLAYER_SPEED = 800.0


class PlayerController:

    def __init__(self, player_object: PlayerData):
        self._player: PlayerData = player_object
        self.input_manager: InputManager = InputManager()
        controllers = get_controllers()
        if controllers:
            self.input_manager.bind_controller(controllers[0])

        self.input_manager.new_action("crouch")
        self.input_manager.subscribe_to_action("crouch", self.set_is_crouching)
        self.input_manager.add_action_input("crouch", Keys.LSHIFT)

        self.input_manager.new_action("grab")
        self.input_manager.subscribe_to_action("grab", self.set_is_grabbing)
        self.input_manager.add_action_input("grab", Keys.SPACE)

        self.input_manager.new_axis("h")
        self.input_manager.add_axis_input("h", Keys.D, scale=1.0)
        self.input_manager.add_axis_input("h", Keys.A, scale=-1.0)
        self.input_manager.add_axis_input("h", ControllerAxes.LEFT_STICK_X)

        self.input_manager.new_axis("v")
        self.input_manager.add_axis_input("v", Keys.W, scale=1.0)
        self.input_manager.add_axis_input("v", Keys.S, scale=-1.0)
        self.input_manager.add_axis_input("v", ControllerAxes.LEFT_STICK_Y)

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
        self.input_manager.update()

        player_move_dir = Vec2(self.input_manager.axis("h"), self.input_manager.axis("v")).normalize()

        self._player.velocity = player_move_dir * PLAYER_SPEED * (1.0 - 0.6 * self._player.is_crouching)
        self._player.origin += self._player.velocity * delta_time
        self._player.direction = player_move_dir
