from typing import Generator, Any
from array import array, ArrayType
from math import ceil

from arcade import get_window, ArcadeContext
import arcade.gl as gl
from pyglet.math import Vec2

from logging import getLogger
from lux.data import get_shader

logger = getLogger("lux")


SPHERE_RADII = (16.0, 6.0, 6.0)
SPHERE_COUNT = len(SPHERE_RADII)

PLAYER_COUNT = 1
PLAYER_PADDING = SPHERE_RADII[0] * 4.0

SMOOTHING_CONST = 1.2

class PlayerSDFRenderer:

    def __init__(self):
        self._ctx: ArcadeContext = None
        self._program: gl.Program = None
        self._geometry: gl.Geometry = None

        self._pos_data: ArrayType = array("f", (0.0,) * PLAYER_COUNT * 2)  # Player Position Vec2 -> (2f)
        self._dir_data: ArrayType = array("f", (0.0,) * PLAYER_COUNT * 2)  # Player Direction Vec2 -> (2f)
        self._colour_data: ArrayType = array("f", (0.0,) * PLAYER_COUNT * 3)  # Player Colour Vec3 -> (3f)
        self._sphere_data: ArrayType = array("f", (0.0,) * PLAYER_COUNT * SPHERE_COUNT * 2) # Sphere Pos 3xVec2 -> (6f)
        self._sphere_aabb: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)

        self._pos_buf: gl.Buffer = None
        self._dir_buf: gl.Buffer = None
        self._colour_buf: gl.Buffer = None
        self._sphere_buf: gl.Buffer = None

        self._has_pos_changed = False
        self._has_dir_changed = False
        self._has_colour_changed = False
        self._have_spheres_changed = False

        self._has_pos_buf_changed = False  # Currently Unused. Would tell Renderer to update CPU buffer.
        self._has_dir_buf_changed = False  # Currently Unused. Would tell Renderer to update CPU buffer.
        self._has_colour_buf_changed = False  # Currently Unused. Would tell Renderer to update CPU buffer.
        self._has_sphere_buf_changed = False  # Currently Unused. Would tell Renderer to update CPU buffer.

        try:
            win = get_window()
            self.init_gl_state()
        except RuntimeError as e:
            logger.error(f"caught error: {e}")

    def init_gl_state(self):
        if self._ctx is not None:
            return

        ctx = get_window().ctx

        self._ctx = ctx

        self._program = self._ctx.program(
            vertex_shader=get_shader("player_sdf_vs"),
            geometry_shader=get_shader("player_sdf_gs"),
            fragment_shader=get_shader("player_sdf_fs")
        )
        self._program["sphere_radii"] = SPHERE_RADII
        self._program["smoothing_const"] = SMOOTHING_CONST

        self._pos_buf: gl.Buffer = ctx.buffer(reserve=PLAYER_COUNT * 8) # 2x32bit
        self._dir_buf: gl.Buffer = ctx.buffer(reserve=PLAYER_COUNT * 8) # 2x32bit
        self._colour_buf: gl.Buffer = ctx.buffer(reserve=PLAYER_COUNT * 12) # 3x32bit
        self._sphere_buf: gl.Buffer = ctx.buffer(reserve=PLAYER_COUNT * 24) # 6x32bit

        content = (
            gl.BufferDescription(self._pos_buf, "2f", ["in_pos"]),
            gl.BufferDescription(self._dir_buf, "2f", ["in_dir"]),
            gl.BufferDescription(self._colour_buf, "3f", ["in_colour"]),
            gl.BufferDescription(self._sphere_buf, "2f 2f 2f", ["in_primary", "in_secondary", "in_tertiary"])
        )

        self._geometry = ctx.geometry(
            content=content
        )

        self._has_pos_changed = True
        self._has_dir_changed = True
        self._has_colour_changed = True
        self._have_spheres_changed = True

    def draw(self):
        self.init_gl_state()
        self._write_sprite_buffers_to_gpu()

        blend_state = self._ctx.is_enabled(self._ctx.BLEND), self._ctx.blend_func

        self._ctx.enable(self._ctx.BLEND)
        self._ctx.blend_func = self._ctx.BLEND_ADDITIVE

        self._geometry.render(
            self._program,
            mode=gl.POINTS
        )

        self._ctx.blend_func = blend_state[-1]
        if not blend_state[0]:
            self._ctx.disable(self._ctx.BLEND)

    def _write_sprite_buffers_to_gpu(self):
        if self._has_pos_changed:
            self._pos_buf.orphan()
            self._pos_buf.write(self._pos_data)
            self._has_pos_changed = False

        if self._has_dir_changed:
            self._dir_buf.orphan()
            self._dir_buf.write(self._dir_data)
            self._has_dir_changed = False

        if self._has_colour_changed:
            self._colour_buf.orphan()
            self._colour_buf.write(self._colour_data)
            self._has_colour_changed = False

        if self._have_spheres_changed:
            self._sphere_buf.orphan()
            self._sphere_buf.write(self._sphere_data)
            self._have_spheres_changed = False

            self._program["player_size"] = ceil(max(self._sphere_aabb[2], self._sphere_aabb[3])) + 2 * PLAYER_PADDING

    def set_pos(self, slot: int, new_pos: Vec2):
        slot *= 2
        self._pos_data[slot] = new_pos.x
        self._pos_data[slot + 1] = new_pos.y

        self._has_pos_changed = True

    def get_pos(self, slot) -> Vec2:
        slot *= 2
        x, y = self._pos_data[slot], self._pos_data[slot + 1]
        return Vec2(x, y)

    def set_dir(self, slot: int, new_dir: Vec2):
        slot *= 2
        self._dir_data[slot] = new_dir.x
        self._dir_data[slot + 1] = new_dir.y

        self._has_dir_changed = True

    def get_dir(self, slot) -> Vec2:
        slot *= 2
        x, y = self._dir_data[slot], self._dir_data[slot + 1]
        return Vec2(x, y)

    def set_colour(self, slot: int, new_colour: tuple[float, float, float]):
        slot *= 3
        self._colour_data[slot] = new_colour[0]
        self._colour_data[slot + 1] = new_colour[1]
        self._colour_data[slot + 2] = new_colour[2]

        self._has_colour_changed = True

    def get_colour(self, slot) -> tuple[float, float, float]:
        slot *= 3
        return self._colour_data[slot], self._colour_data[slot + 1], self._colour_data[slot + 2]

    def set_spheres(self, slot: int, new_primary: Vec2 = None, new_secondary: Vec2 = None, new_tertiary: Vec2 = None):
        # I hate everything about this

        if not any((new_primary, new_secondary, new_tertiary)):
            return

        new_min_x = new_min_y = float("inf")
        new_max_x = new_max_y = -float("inf")

        slot *= 2 * SPHERE_COUNT
        if new_primary:
            self._sphere_data[slot] = new_primary.x
            self._sphere_data[slot + 1] = new_primary.y
            self._have_spheres_changed = True

            new_min_x = min(new_primary.x, new_min_x)
            new_max_x = max(new_primary.x, new_max_x)

            new_min_y = min(new_primary.y, new_min_y)
            new_max_y = max(new_primary.y, new_max_y)
        else:
            x, y = self._sphere_data[slot], self._sphere_data[slot + 1]

            new_min_x = min(x, new_min_x)
            new_max_x = max(x, new_max_x)

            new_min_y = min(y, new_min_y)
            new_max_y = max(y, new_max_y)

        if new_secondary:
            self._sphere_data[slot + 2] = new_secondary.x
            self._sphere_data[slot + 3] = new_secondary.y
            self._have_spheres_changed = True

            new_min_x = min(new_secondary.x, new_min_x)
            new_max_x = max(new_secondary.x, new_max_x)

            new_min_y = min(new_secondary.y, new_min_y)
            new_max_y = max(new_secondary.y, new_max_y)
        else:
            x, y = self._sphere_data[slot + 2], self._sphere_data[slot + 3]

            new_min_x = min(x, new_min_x)
            new_max_x = max(x, new_max_x)

            new_min_y = min(y, new_min_y)
            new_max_y = max(y, new_max_y)

        if new_tertiary:
            self._sphere_data[slot + 4] = new_tertiary.x
            self._sphere_data[slot + 5] = new_tertiary.y
            self._have_spheres_changed = True

            new_min_x = min(new_tertiary.x, new_min_x)
            new_max_x = max(new_tertiary.x, new_max_x)

            new_min_y = min(new_tertiary.y, new_min_y)
            new_max_y = max(new_tertiary.y, new_max_y)
        else:
            x, y = self._sphere_data[slot + 4], self._sphere_data[slot + 5]

            new_min_x = min(x, new_min_x)
            new_max_x = max(x, new_max_x)

            new_min_y = min(y, new_min_y)
            new_max_y = max(y, new_max_y)

        if self._have_spheres_changed:
            self._sphere_aabb = new_min_x, new_min_y, (new_max_x - new_min_x), (new_max_y - new_min_y)

    def get_spheres(self, slot: int) -> Generator[Vec2, Any, None]:
        slot *= 2 * SPHERE_COUNT
        s = self._sphere_data[slot:slot+2*SPHERE_COUNT]
        return (Vec2(s[2*idx], s[2*idx + 1]) for idx in range(0, SPHERE_COUNT))