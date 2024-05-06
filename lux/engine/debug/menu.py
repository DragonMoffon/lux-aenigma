from __future__ import annotations

import typing
import arcade

import imgui
from imgui.integrations.pyglet import create_renderer

if typing.TYPE_CHECKING:
    from lux.setup.lux_window import LuxWindow

class DebugMenu(typing.Protocol):

    def draw(self):
        ...


class DebugDisplay:

    def __init__(self, window: LuxWindow):
        imgui.create_context()
        imgui.get_io().display_size = 100, 100
        imgui.get_io().fonts.get_tex_data_as_rgba32()
        self.renderer = create_renderer(window)
        self.current_menu: DebugMenu = None
        self.show = True

    def draw(self):
        if self.current_menu is not None and self.show:
            self.renderer.process_inputs()
            self.current_menu.draw()

            imgui.render()
            self.renderer.render(imgui.get_draw_data())

    def set_menu(self, new_menu: DebugMenu):
        self.current_menu = new_menu
