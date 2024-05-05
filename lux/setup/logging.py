import logging

from digiformatter import logger as digilogger


def setup_logging():
    logging.basicConfig(level=logging.INFO)
    dfhandler = digilogger.DigiFormatterHandler()
    dfhandlersource = digilogger.DigiFormatterHandler(showsource=True)

    logger = logging.getLogger("lux")
    logger.setLevel(logging.DEBUG)
    logger.handlers = []
    logger.propagate = False
    logger.addHandler(dfhandler)

    arcadelogger = logging.getLogger("arcade")
    arcadelogger.setLevel(logging.WARN)
    arcadelogger.handlers = []
    arcadelogger.propagate = False
    arcadelogger.addHandler(dfhandlersource)