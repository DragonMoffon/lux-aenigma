from lux.engine.lights import Ray


class RayDebugRenderer:

    def __init__(self, child: Ray):
        self._child = child
