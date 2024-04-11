import importlib.resources as pkg_resources

import lux.shaders


def get_shader(name: str) -> str:
    shader_name = name + ".glsl"
    s = pkg_resources.read_text(lux.shaders, shader_name)
    return s
