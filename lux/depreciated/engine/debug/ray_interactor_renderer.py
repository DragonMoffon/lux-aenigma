from arcade import draw_line, draw_point

from lux.depreciated.engine.interactors import RayInteractor


class RayInteractorRenderer:

    def __init__(self, child: RayInteractor):
        self.child: RayInteractor = child

    def draw(self):
        edges = self.child.bounds
        colour = self.child.colour.to_int_color()
        position = self.child.origin
        heading = self.child.direction.heading
        for edge in edges:
            start, end, center, normal = (
                position + edge.start.rotate(heading),
                position + edge.end.rotate(heading),
                position + edge.center.rotate(heading),
                edge.normal.rotate(heading)
            )

            draw_line(start.x, start.y, end.x, end.y, colour, 2.0)
            draw_line(center.x, center.y, center.x + normal.x * 15.0, center.y + normal.y * 15.0, colour, 2.0)
            draw_point(start.x, start.y, colour, 4.0)

    def update_child(self, new_child: RayInteractor):
        self.child = new_child
