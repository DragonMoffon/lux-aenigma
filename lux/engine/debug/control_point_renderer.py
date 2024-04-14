from lux.engine.control_points.control_point import ControlPoint
from lux.util.draw import draw_cross


class ControlPointRenderer:
    def __init__(self, child: ControlPoint):
        self.child: ControlPoint = child

    def update_child(self, new_child: ControlPoint):
        self.child = new_child

    def draw(self):
        a_p = self.child.absolute_position
        draw_cross(a_p, 4, self.child.colour, 1)
