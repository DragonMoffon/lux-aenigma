from arcade.draw_commands import draw_point

from lux.engine.control_points.control_point import ControlPoint


class ControlPointRenderer:
    def __init__(self, child: ControlPoint):
        self.child: ControlPoint = child

    def update_child(self, new_child: ControlPoint):
        self.child = new_child

    def draw(self):
        a_p = self.child.absolute_position
        draw_point(a_p.x, a_p.y, self.child.colour.to_int_color(), 5.0)
