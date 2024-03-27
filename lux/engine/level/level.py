from lux.engine.level.level_object import LevelObject


class Level:
    """
    A single level which is equal to one "puzzle".
    """
    def __init__(self):
        self._notifiers: object = None
        self._objects: set[LevelObject] = set()
