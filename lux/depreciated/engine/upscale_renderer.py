from contextlib import contextmanager

import arcade.gl as gl
from arcade import get_window, ArcadeContext

v_shader = """#version 330
in vec2 in_uv;
in vec2 in_vert;
out vec2 out_uv;
void main(){
out_uv = in_uv;
gl_Position = vec4(in_vert, 0.0, 1.0);
}
"""
f_shader = """#version 330
uniform sampler2D texture0;
in vec2 out_uv;
out vec4 out_colour;
void main(){
out_colour = texture(texture0, out_uv);
}"""


class UpscaleBuffer:
    quad_geometry: gl.Geometry | None = None

    def __init__(self, width: int, height: int, components: int = 4, dtype: str = 'f1'):
        if UpscaleBuffer.quad_geometry is None:
            UpscaleBuffer.quad_geometry = gl.geometry.quad_2d_fs()

        self._ctx: ArcadeContext = get_window().ctx
        self._w = width
        self._h = height

        self._texture: gl.Texture2D = self._ctx.texture(
            (width, height),
            components=components,
            dtype=dtype,
            filter=(gl.NEAREST, gl.NEAREST)
        )

        self._buffer: gl.Framebuffer = self._ctx.framebuffer(
            color_attachments=[self._texture]
        )

        self._draw_program = self._ctx.program(
            vertex_shader = v_shader,
            fragment_shader = f_shader
        )

    @contextmanager
    def activate(self):
        prev_fbo = self._ctx.active_framebuffer
        try:
            self._buffer.use()
            yield self._buffer
        finally:
            prev_fbo.use()

    def use(self):
        self._buffer.use()

    def clear(self):
        self._buffer.clear()

    @property
    def texture(self):
        return self._texture

    def draw(self):
        self._texture.use()
        UpscaleBuffer.quad_geometry.render(self._draw_program)
