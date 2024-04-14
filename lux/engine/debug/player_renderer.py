from lux.engine.player.player_object import PlayerData
from lux.util.draw import draw_cross


class PlayerDebugRenderer:
    def __init__(self, child: PlayerData):
        self.child: PlayerData = child

    def update_child(self, new_child: PlayerData):
        self.child = new_child

    def draw(self):
        c = self.child.colour
        o = self.child.origin
        draw_cross(o, 7.5, c, 2)
