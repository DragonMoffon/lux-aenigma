from __future__ import annotations

import typing

import imgui
from imgui.integrations.pyglet import create_renderer

if typing.TYPE_CHECKING:
    from lux.setup.lux_window import LuxWindow

class DebugDisplay:

    def __init__(self, window: LuxWindow):
        imgui.create_context()
        imgui.get_io().display_size = 100, 100
        imgui.get_io().fonts.get_tex_data_as_rgba32()
        self.renderer = create_renderer(window)
        self.current_menu: typing.Callable = None
        self.show = True

    def draw(self):
        if self.current_menu is not None and self.show:
            self.renderer.process_inputs()
            self.current_menu()

            imgui.render()
            self.renderer.render(imgui.get_draw_data())

    def set_menu(self, new_menu: typing.Callable):
        self.current_menu = new_menu
