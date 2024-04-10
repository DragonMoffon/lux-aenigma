from arcade import draw_line

from lux.engine.player.player_object import PlayerData


OFFSET = 7.5


class PlayerDebugRenderer:
    def __init__(self, child: PlayerData):
        self.child: PlayerData = child

    def update_child(self, new_child: PlayerData):
        self.child = new_child

    def draw(self):
        c = self.child.colour.to_int_color()
        o = self.child.origin
        draw_line(
            o.x - OFFSET, o.y - OFFSET,
            o.x + OFFSET, o.y + OFFSET,
            c,
            2.0
        )
        draw_line(
            o.x + OFFSET, o.y - OFFSET,
            o.x - OFFSET, o.y + OFFSET,
            c,
            2.0
        )
