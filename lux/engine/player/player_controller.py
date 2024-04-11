from pyglet.math import Vec2

from lux.engine.input import InputManager, ActionState

from lux.engine.input.inputs import Keys
from lux.engine.player.player_object import PlayerData


class PlayerController:

    def __init__(self, player_object: PlayerData):
        self._player: PlayerData = player_object
        self.input_manager: InputManager = InputManager()

        self.input_manager.new_action("jump")
        self.input_manager.add_action_input("jump", Keys.SPACE)
        self.input_manager.subscribe_to_action("jump", self.player_jump)

        self.t = 0.0

    def player_jump(self, action_state: ActionState):
        pass

    def update(self, delta_time):
        self.t += delta_time

        self._player.origin = Vec2(400, 400) + Vec2(100.0, 0.0).rotate(self.t)
