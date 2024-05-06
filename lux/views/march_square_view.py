import arcade
from arcade.experimental.input.inputs import MouseButtons, Keys
from arcade.draw_commands import draw_triangle_outline, draw_triangle_filled

from lux.util.view import LuxView

GRID_WIDTH = 11
GRID_HEIGHT = 11

SQUARE_SIZE = 50

triangulations = (
    (), # 0000
    ((0, 1, 7),), # 0001 x=0 (x, x+1, x-1)
    ((2, 3, 1),), # 0010 x=2 (x, x+1, x-1)
    ((0, 2, 7), (7, 2, 3),), # 0011 x=0 (x, x+2, x-1) (x-1, x+2, x+3)
    ((4, 3, 5),), # 0100 x=4 (x, x+1, x-1)
    ((0, 1, 7), (7, 1, 3), (7, 3, 5), (3, 4, 5),), # 0101 x=0 (x, x+1, x-1) (x-1, x+1, x+3) (x-1, x+3, x+5) (x+3, x+4, x+5)
    ((2, 4, 1), (1, 4, 5),), # 0110 x=2 (x, x+2, x-1) (x-1, x+2, x+3)
    ((2, 4, 5), (2, 5, 7), (2, 7, 0),), # 0111 x=2 (x, x+2, x+3) (x, x+3, x+5) (x, x+5, x+6)
    ((6, 7, 5),), # 1000 x=6 (x, x+1, x-1)
    ((6, 0, 5), (5, 0, 1),), # 1001 x=6 (x, x+2, x-1) (x-1, x+2, x+3)
    ((2, 3, 1), (1, 3, 5), (1, 5, 7), (5, 6, 7),), # 1010 x=2 (x, x+1, x-1) (x-1, x+1, x+3) (x-1, x+3, x+5) (x+3, x+4, x+5)
    ((0, 2, 3), (0, 3, 5), (0, 5, 6),), # 1011 x=0  (x, x+2, x+3) (x, x+3, x+5) (x, x+5, x+6)
    ((4, 6, 3), (3, 6, 7),), # 1100 x=4 (x, x+2, x-1) (x-1, x+2, x+3)
    ((6, 0, 1), (6, 1, 3), (6, 3, 4),), # 1101 x=6 (x, x+2, x+3) (x, x+3, x+5) (x, x+5, x+6)
    ((4, 6, 7), (4, 7, 1), (4, 1, 2),), # 1110 x=4 (x, x+2, x+3) (x, x+3, x+5) (x, x+5, x+6)
    ((0, 2, 4), (0, 4, 6),), # 1111 x=0 (x, x+2, x-2), (x-2, x+2, x+4)
)

class MarchGrid:

    def __init__(self):
        self.grid = list(
            list(-1.0 for _ in range(GRID_WIDTH))
            for _ in range(GRID_HEIGHT)
        )

    def __getitem__(self, item: tuple[int, int]):
        x, y = item
        return self.grid[y][x]

    def __setitem__(self, key: tuple[int, int], value: float):
        x, y = key
        self.grid[y][x] = min(1.0, max(-1.0, value))

    def closest_point(self, x: float, y: float):
        s_x = x / SQUARE_SIZE
        s_y = y / SQUARE_SIZE

        i_x = int(round(s_x))
        i_y = int(round(s_y))

        return i_x, i_y

    def set_closest_point(self, x: float, y: float, value: float):
        i_x, i_y = self.closest_point(x, y)

        if 0 <= i_x < GRID_WIDTH and 0 <= i_y < GRID_HEIGHT:
            self[i_x, i_y] = value

    def get_closest_point(self, x, y):
        i_x, i_y = self.closest_point(x, y)
        if 0 <= i_x < GRID_WIDTH and 0 <= i_y < GRID_HEIGHT:
            return self[i_x, i_y]
        return None

    def triangulate_point(self, x: int, y: int):
        a = self.grid[y][x]
        b = self.grid[y+1][x]
        c = self.grid[y+1][x+1]
        d = self.grid[y][x+1]

        a_b = (0.5 if a == b else (1.0 if b == 0.0 else -a/(b - a)))
        b_c = (0.5 if b == c else (1.0 if c == 0.0 else -b/(c - b)))
        d_c = (0.5 if d == c else (1.0 if c == 0.0 else -d/(c - d)))
        a_d = (0.5 if a == d else (1.0 if d == 0.0 else -a/(d - a)))

        idx = (a > 0) * 1 + (b > 0) * 2 + (c > 0) * 4 + (d > 0) * 8
        triangulation = triangulations[idx]
        points = (
            (x, y), (x, y+a_b),
            (x, y+1), (x+b_c, y+1),
            (x+1, y+1), (x+1, y+d_c),
            (x+1, y), (x+a_d, y)
        )

        return (tuple(points[i] for i in tri) for tri in triangulation)

    def draw(self):
        for y, row in enumerate(self.grid[:]):
            for x, val in enumerate(row[:]):
                if x < GRID_WIDTH-1 and y < GRID_HEIGHT-1:
                    triangles = self.triangulate_point(x, y)
                    for tri in triangles:
                        a, b, c = tri
                        draw_triangle_filled(
                            a[0]*SQUARE_SIZE, a[1]*SQUARE_SIZE,
                            b[0]*SQUARE_SIZE, b[1]*SQUARE_SIZE,
                            c[0]*SQUARE_SIZE, c[1]*SQUARE_SIZE,
                            (255, 255, 255, 255)# , 2
                        )
                c = (255 * (val < 0), 255 * (val > 0),  255, 255)
                arcade.draw_point(x * SQUARE_SIZE, y * SQUARE_SIZE, c, 5)


class SquareView(LuxView):

    def __init__(self, back: LuxView):
        super().__init__(back=back)

        self.cam = arcade.camera.Camera2D(position=(0.0, 0.0))
        self.grid = MarchGrid()

        self.grid[0, 0] = 1
        self.grid[0, 1] = 1
        self.grid[2, 3] = 1

        self.grid.triangulate_point(0, 0)
        self.grid.triangulate_point(0, 1)

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, _buttons: int, _modifiers: int):
        try:
            button = MouseButtons(_buttons)
        except ValueError:
            return 

        if button == MouseButtons.MIDDLE:
            o_pos = self.cam.position
            self.cam.position = int(o_pos[0] - dx), int(o_pos[1] - dy)
        elif button == MouseButtons.LEFT:
            w_x, w_y, w_z = self.cam.unproject((x, y))
            self.grid.set_closest_point(w_x, w_y, 1)
        elif button == MouseButtons.RIGHT:
            w_x, w_y, w_z = self.cam.unproject((x, y))
            self.grid.set_closest_point(w_x, w_y, -1)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        button = MouseButtons(button)

        if button == MouseButtons.LEFT:
            w_x, w_y, w_z = self.cam.unproject((x, y))
            self.grid.set_closest_point(w_x, w_y, 1)

        elif button == MouseButtons.RIGHT:
            w_x, w_y, w_z = self.cam.unproject((x, y))
            self.grid.set_closest_point(w_x, w_y, -1)

    def on_key_press(self, symbol: int, modifiers: int):
        super().on_key_press(symbol, modifiers)

    def on_update(self, delta_time: float):
        return super().on_update(delta_time)

    def on_draw(self):
        self.clear()
        self.cam.use()

        self.grid.draw()
