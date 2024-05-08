import importlib.resources as pkg_resources
from PIL import Image
from tomlkit import parse, dumps, TOMLDocument


from arcade import load_sound, Sound, text, load_texture, Texture

import lux.data.config as config
import lux.data.fonts as fonts
import lux.data.levels as levels
import lux.data.music as music
import lux.data.sfx as sfx
import lux.data.shaders as shaders
import lux.data.textures as textures


def get_config(name: str) -> TOMLDocument:
    config_name = name + ".toml"
    s = pkg_resources.read_text(config, config_name)
    return parse(s)


def save_config(name: str, data: TOMLDocument) -> None:
    config_name = name + ".toml"
    s = dumps(data, sort_keys=False)
    with pkg_resources.path(config, config_name) as path:
        with open(path, "w") as file:
            file.write(s)


def load_font(name: str) -> None:
    font_name = name + ".ttf"
    with pkg_resources.path(fonts, font_name) as path:
        text.load_font(path)


def get_shader(name: str) -> str:
    shader_name = name + ".glsl"
    s = pkg_resources.read_text(shaders, shader_name)
    return s


def get_music(name: str, streaming: bool = False,  *, file_type: str = "mp3") -> Sound:
    music_name = f"{name}.{file_type}"
    with pkg_resources.path(music, music_name) as path:
        return load_sound(path, streaming)


def get_sfx(name: str, *, file_type: str = "wav") -> Sound:
    sfx_name = f"{name}.{file_type}"
    with pkg_resources.path(sfx, sfx_name) as path:
        return load_sound(path, streaming=False)


def get_image(name: str, file_type: str = "png") -> Image:
    image_name = f"{name}.{file_type}"
    with pkg_resources.path(textures, image_name) as path:
        return Image.open(path)


def get_texture(name: str, *, file_type: str = "png",
                x: int = 0, y: int = 0, width: int = 0, height: int = 0, hit_box_alg=None) -> Texture:
    texture_name = f"{name}.{file_type}"
    with pkg_resources.path(textures, texture_name) as path:
        return load_texture(path, x=x, y=y, width=width, height=height, hit_box_algorithm=hit_box_alg)


def get_level_data(name: str) -> TOMLDocument:
    level_name = f"{name}.toml"
    s = pkg_resources.read_text(levels, level_name)
    return parse(s)


def save_level_data(name: str, data: TOMLDocument):
    level_name = f"{name}.toml"
    with pkg_resources.path(levels, level_name) as path:
        with open(path, 'w') as level_file:
            level_file.write(dumps(data))