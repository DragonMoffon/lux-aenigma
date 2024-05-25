from lux.util import draw_cross

from weakref import WeakSet, proxy, ProxyType

from util.uuid_ref import UUIDRef

from lux.components import ControlPoint, Player, LevelObject
from lux.systems.base import System, _ComponentSource

from lux.consts import CONSTS


class ControlPointSystem(System):
    requires = frozenset((ControlPoint, Player))

    def __init__(self):
        super().__init__()

        self._control_points: WeakSet[ControlPoint] = None
        self._control_point_parent_map: dict[int, UUIDRef[LevelObject]] = None

        self._player_data: ProxyType[Player] = None
        self._player_object: UUIDRef[LevelObject] = None

    def preload(self):
        self._control_points = None
        self._player_data = None
        self._player_object = None

        self._control_point_parent_map = dict()

    def unload(self):
        self._player_data = None
        self._player_object = None

        self._control_points = None
        self._control_point_parent_map = None

    def load(self, source: _ComponentSource):
        self._control_points = source.get_components(ControlPoint)
        for control_point in self._control_points:
            self._control_point_parent_map[control_point.UUID] = control_point.parent
            for dof in control_point.dof:
                dof.retrieve()

        player_set = source.get_components(Player)
        self._player_data = proxy(tuple(player_set)[0])
        self._player_object = self._player_data.parent

    def draw(self):
        for control_point in self._control_points:
            parent: LevelObject = self._control_point_parent_map[control_point.UUID]
            d = parent.direction
            n = parent.normal
            pos = control_point.relative.x * d + control_point.relative.y * n
            draw_cross(parent.origin + pos, 10, control_point.colour)

    def update(self, dt):
        if not self._player_data.is_grabbing:
            self._player_data.grabbed_control_point = None
            return

        if self._player_data.grabbed_control_point is not None:
            control_point = self._player_data.grabbed_control_point
            parent: LevelObject = self._control_point_parent_map[control_point.UUID]
            d = parent.direction
            n = parent.normal
            pos = parent.origin + control_point.relative.x * d + control_point.relative.y * n
            diff = pos - self._player_object.origin
            dist = diff.dot(diff)
            if dist < CONSTS['PLAYER_GRAB_RADIUS']**2:
                for dof in control_point.dof:
                    dof.pull(parent, pos, self._player_object.origin, self._player_data.velocity * dt)
                return

            if dist > CONSTS['PLAYER_RELEASE_RADIUS']**2:
                self._player_data.grabbed_control_point = None  # Maybe change this?
            return

        closest_dist = CONSTS['PLAYER_RELEASE_RADIUS']**2
        closest_point = None
        for control_point in self._control_points:
            parent: LevelObject = self._control_point_parent_map[control_point.UUID]
            d = parent.direction
            n = parent.normal
            pos = parent.origin + control_point.relative.x * d + control_point.relative.y * n
            diff = pos - self._player_object.origin
            if diff.dot(diff) < closest_dist:
                closest_point = control_point
                closest_dist = diff.dot(diff)

        if closest_point is None:
            self._player_data.grabbed_control_point = None
        else:
            self._player_data.grabbed_control_point = proxy(closest_point)
