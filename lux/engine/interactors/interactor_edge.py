from __future__ import annotations

from pyglet.math import Vec2


class RayInteractorEdge:
    __slots__ = (
        "_start",
        "_end",
        "_direction",
        "_normal",
        "_bi_dir"
    )

    def __init__(self, start: Vec2, end: Vec2, bi_dir: bool):
        self._start: Vec2 = start
        self._end: Vec2 = end

        self._direction = (end - start).normalize()
        self._normal: Vec2 = Vec2(self._direction.y, -self._direction.x)

        self._bi_dir: bool = bi_dir

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other: RayInteractorEdge):
        return self._start == other.start and self._end == other.end and self._bi_dir == other._bi_dir

    def __str__(self):
        return f"{self._start=}, {self._end=}, {self._bi_dir=}"

    def __repr__(self) -> str:
        return f"RayInteractorEdge<{self._start}>"

    @property
    def center(self):
        return (self._start + self._end) / 2.0

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def direction(self):
        return self._direction

    @property
    def normal(self):
        return self._normal

    @property
    def bi_dir(self):
        return self._bi_dir

    def adjust(self, origin: Vec2, heading: float):
        return RayInteractorEdge(
            origin + self._start.rotate(heading),
            origin + self._end.rotate(heading),
            self._bi_dir
        )