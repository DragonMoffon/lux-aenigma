from __future__ import annotations
from typing import TypedDict
from enum import Enum
from weakref import ProxyType

from pyglet.math import Vec2

from lux.components.base import Component, Resolvable
from lux.components.core import LevelObject
from lux.components.control import ControlPoint

from util.uuid_ref import UUIDRef

class PlayerState(Enum):
    IDLING = 0
    MOVING = 1
    CROUCHING = 2
    CRAWLING = 3
    GRABBING = 4
    PULLING = 5


PlayerDict = TypedDict(
    'PlayerDict',
    {
        'UUID': int,
        'parent': int
    }
)


# Currently the player origin etc. are stored as a LevelObject separately, but maybe due to how often they change
# It should all be rolled into one? Idk yet.

class Player(Component):

    def __init__(self, UUID: int, parent: UUIDRef[LevelObject]):
        super().__init__(UUID)
        self.parent: UUIDRef[LevelObject] = parent

        # State
        self.state: PlayerState = PlayerState.IDLING

        # movement variables
        self.velocity: Vec2 = Vec2()
        self.is_crouching: bool = False

        # Control point Variable
        self.is_grabbing: bool = False

        # We use a proxy type rather than a UUID ref because we get it at run time rather than statically at startup.
        self.grabbed_control_point: ProxyType[ControlPoint] | None = None

    def serialise(self) -> PlayerDict:
        return {
            'UUID': self.UUID,
            'parent': self.parent._val
        }

    @classmethod
    def deserialise(cls, data: PlayerDict) -> tuple[Player, tuple[Resolvable, ...]]:
        UUID = data['UUID']
        parent_ref = UUIDRef(data['parent'])

        return Player(UUID, parent_ref), (parent_ref,)