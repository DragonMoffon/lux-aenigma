from __future__ import annotations
from typing import Union, Any, TypedDict

from pyglet.math import Vec2

from lux.util import LuxColour

from lux.components.base import Component, Resolvable

from util.uuid_ref import UUIDRef


class DegreeOfFreedom:

    def pull(self, parent: Component, control_point_pos: Vec2, lux_pos: Vec2, lux_velocity: Vec2, control_point_weight: float):
        raise NotImplementedError()

    @classmethod
    def serialise(cls) -> dict:
        raise NotImplementedError()

    @classmethod
    def deserialise(cls, data) -> DegreeOfFreedom:
        raise NotImplementedError()


class RotationDOF(DegreeOfFreedom):
    pass


class AxisDOF:

    def __init__(self, axis: Vec2, origin: Vec2, min_offset: float = -float('inf'), max_offset: float = float('inf')):
        self.axis: Vec2 = axis
        self.origin: Vec2 = origin
        self.min_offset: float = min_offset
        self.max_offset: float = max_offset

    def pull(self, parent: Component, control_point_pos: Vec2, lux_pos: Vec2, lux_velocity: Vec2, control_point_weight: float):
        """
        I HATE this function
        """

class ToggleDOF:
    pass

# Vomiting everywhere
_DOF_MAP: dict[str, type[DegreeOfFreedom]] = {dof.__name__: dof for dof in DegreeOfFreedom.__subclasses__()}

ControlPointDict = TypedDict(
    'ControlPointDict',
    {
        'UUID': int,
        'parent': int,
        'relative': tuple[float, float],
        'colour': tuple[bool, bool, bool],
        'dof': tuple
    }
)

class ControlPoint(Component):

    def __init__(self, UUID: int, parent: UUIDRef[Component], relative: Vec2, colour: LuxColour, dof: tuple[DegreeOfFreedom, ...]):
        super().__init__(UUID)
        self.parent: UUIDRef[Component] = parent
        self.relative: Vec2 = Vec2(relative[0], relative[1])
        self.colour: LuxColour = colour
        self.dof: tuple[DegreeOfFreedom, ...] = dof

    def serialise(self) -> ControlPointDict:
        raise NotImplementedError()

    @classmethod
    def deserialise(cls, data: ControlPointDict) -> tuple[ControlPoint, tuple[Resolvable, ...]]:
        raise NotImplementedError()
