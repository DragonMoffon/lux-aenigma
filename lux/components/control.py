from typing import Union, Any, TypedDict

from pyglet.math import Vec2

from components.base import Resolvable
from lux.util import LuxColour

from lux.components.base import Component

from util.uuid_ref import UUIDRef

class RotationDOF:
    pass


class AxisDOF:
    pass


class ToggleDOF:
    pass


DegreeOfFreedom = Union[RotationDOF, AxisDOF, ToggleDOF]

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
    def deserialise(cls, data: ControlPointDict) -> tuple[Any, tuple[Resolvable, ...]]:
        raise NotImplementedError()
