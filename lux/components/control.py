from __future__ import annotations
from typing import Union, Any, TypedDict

from pyglet.math import Vec2

from lux.util import LuxColour

from lux.components.base import Component, Resolvable
from lux.components.core import LevelObject

from util.uuid_ref import UUIDRef
from lux.util.maths import clamp


class DegreeOfFreedom[T: Component]:

    def __init__(self, target: UUIDRef[T]):
        self._target: UUIDRef[T] = target

    def retrieve(self):
        """
        Collect any data which requires UUIDRefs to be resolved
        """
        pass

    def pull(self, parent: LevelObject, control_point_pos: Vec2, lux_pos: Vec2, lux_velocity: Vec2):
        raise NotImplementedError()

    def serialise(self) -> dict[str, Any]:
        raise NotImplementedError()

    @classmethod
    def deserialise(cls, data: dict) -> tuple[DegreeOfFreedom, Resolvable]:
        raise NotImplementedError()


class Rotation(DegreeOfFreedom):
    pass


AxisDOFDict = TypedDict(
    'AxisDOFDict',
    {
        'type': str,
        'target': int,
        'axis': list[float],
        'min': float,
        'max': float
    }
)

class Axis(DegreeOfFreedom[LevelObject]):

    def __init__(self, target: UUIDRef[LevelObject], axis: Vec2, min_offset: float = -float('inf'), max_offset: float = float('inf')):
        super().__init__(target)
        self.axis: Vec2 = axis
        self.origin: Vec2 = None
        self.min_offset: float = min_offset
        self.max_offset: float = max_offset

    def retrieve(self):
        self.origin = self._target.origin

    def serialise(self) -> AxisDOFDict:
        return {
            'type': self.__name__,
            'target': self._target.UUID,
            'axis': [self.axis.x,self.axis.y],
            'min': self.min_offset,
            'max': self.max_offset
        }

    @classmethod
    def deserialise(cls, data: AxisDOFDict) -> tuple[Axis, UUIDRef]:
        target_ref = UUIDRef(data['target'])
        axis = Vec2(data['axis'][0], data['axis'][1])
        return Axis(target_ref, axis, data['min'], data['max']), target_ref

    def pull(self, parent: LevelObject, control_point_pos: Vec2, lux_pos: Vec2, lux_velocity: Vec2):
        print()
        pull_str = self.axis.dot(lux_velocity.normalize())
        pull_qual = self.axis.dot((lux_pos - control_point_pos).normalize())

        if not pull_qual or pull_str / pull_qual <= 0.0:
            return

        print(pull_str)
        diff = self.axis.dot(self._target.origin - self.origin)
        print(diff)
        final_pull = clamp(self.min_offset, diff + pull_str, self.max_offset) - diff
        print(final_pull)
        self._target.origin = self._target.origin + self.axis * final_pull


_DOF_MAP: dict[str, type[DegreeOfFreedom]] = {dof.__name__: dof for dof in DegreeOfFreedom.__subclasses__()}



ControlPointDict = TypedDict(
    'ControlPointDict',
    {
        'UUID': int,
        'parent': int,
        'relative': tuple[float, float],
        'colour': tuple[bool, bool, bool],
        'dof': tuple[dict[str, Any], ...]
    }
)

class ControlPoint(Component):

    def __init__(self, UUID: int, parent: UUIDRef[LevelObject], relative: Vec2, colour: LuxColour, dof: tuple[DegreeOfFreedom, ...]):
        super().__init__(UUID)
        self.parent: UUIDRef[LevelObject] = parent
        self.relative: Vec2 = Vec2(relative[0], relative[1])
        self.colour: LuxColour = colour
        self.dof: tuple[DegreeOfFreedom, ...] = dof

    def serialise(self) -> ControlPointDict:
        return {
            'UUID': self.UUID,
            'parent': self.parent.UUID,
            'relative': (self.relative.x, self.relative.y),
            'colour': (self.colour.red, self.colour.green, self.colour.blue),
            'dof': tuple(dof.serialise() for dof in self.dof)
        }

    @classmethod
    def deserialise(cls, data: ControlPointDict) -> tuple[ControlPoint, tuple[Resolvable, ...]]:
        parent = UUIDRef(data['parent'])
        relative = Vec2(*data['relative'])
        color = LuxColour(*data['colour'])

        dofs, targets = zip(*tuple(_DOF_MAP[dof['type']].deserialise(dof) for dof in data['dof']))
        return ControlPoint(data['UUID'], parent, relative, color, dofs), (parent,) + targets
