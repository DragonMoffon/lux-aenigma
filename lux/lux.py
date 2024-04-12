from pathlib import Path
import importlib.resources as pkg_resources
import logging

from digiformatter import logger as digilogger
import arcade
import lux.data.fonts

from lux import get_window


with pkg_resources.path(lux.data.fonts, "gohu.ttf") as p:
    arcade.text.load_font(str(p))


def setup_logging():
    logging.basicConfig(level=logging.INFO)
    dfhandler = digilogger.DigiFormatterHandler()
    dfhandlersource = digilogger.DigiFormatterHandler(showsource=True)

    logger = logging.getLogger("lux")
    logger.setLevel(logging.WARN)
    logger.handlers = []
    logger.propagate = False
    logger.addHandler(dfhandler)

    arcadelogger = logging.getLogger("arcade")
    arcadelogger.setLevel(logging.WARN)
    arcadelogger.handlers = []
    arcadelogger.propagate = False
    arcadelogger.addHandler(dfhandlersource)


def main():
    setup_logging()
    arcade.resources.add_resource_handle("textures", (Path() / Path("lux/data/textures").resolve()))
    get_window().run()


if __name__ == "__main__":
    main()
