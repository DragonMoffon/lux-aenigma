from __future__ import annotations

from typing import Protocol, Any
from weakref import ReferenceType, ref


class _UUIDMap(Protocol):
    UUID_map: dict[int, Any]

    def resolve_UUID(self, UUID_: int) -> Any:
        ...

class UUIDRef[R]:

    def __init__(self, val: int):
        self._ref: ReferenceType[R] = None
        self._val: int = val

    @property
    def value(self):
        return self._val

    def resolve(self, source: _UUIDMap):
        if self._ref is not None:
            raise ValueError("object has been resolved already")
        ref_ = source.resolve_UUID(self._val)

        self._ref = ref(ref_)

    def __getattr__(self, item: str):
        if item.startswith("_"):
            return self.__dict__[item]

        ref_ = self._ref()
        if ref_ is None:
            raise ValueError("object has been garbage collected")

        return getattr(ref_, item)
    def __setattr__(self, key: str, value):
        if key.startswith("_"):
            self.__dict__[key] = value
            return

        ref_ = self._ref()
        if ref_ is None:
            raise ValueError("object has been garbage collected")

        setattr(ref_, key, value)
