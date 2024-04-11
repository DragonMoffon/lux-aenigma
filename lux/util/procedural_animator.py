from math import pi, tau

from typing import TypeVar, Protocol, Optional


__all__ = (
    'SecondOrderAnimator',
)


class Animatable(Protocol):

    def __mul__(self, other):
        ...

    def __add__(self, other):
        ...

    def __sub__(self, other):
        ...


A = TypeVar('A', bound=Animatable)


class SecondOrderAnimator:

    def __init__(self, frequency: float, damping: float, response: float,  x_initial: A, y_initial: A, y_d_initial: A):
        self.xp: Animatable = x_initial
        self.y: Animatable = y_initial
        self.dy: Optional[Animatable] = y_d_initial

        self._freq = frequency
        self._damp = damping
        self._resp = response

        self.k1: float = damping / (pi * frequency)
        self.k2: float = 1.0 / (tau * frequency)**2.0
        self.k3: float = (response * damping) / (tau * frequency)

    def update_frequency(self, new_frequency):
        self._freq = new_frequency
        self.calc_k_vals()

    def update_damping(self, new_damping):
        self._damp = new_damping
        self.calc_k_vals()

    def update_response(self, new_response):
        self._resp = new_response
        self.calc_k_vals()

    def update_vals(self, new_frequency: Optional[A], new_damping: Optional[A], new_response: Optional[A]):
        self._freq = new_frequency or self._freq
        self._damp = new_damping or self._damp
        self._resp = new_response or self._resp

        self.calc_k_vals()

    def calc_k_vals(self):
        self.k1 = self._damp / (pi * self._freq)
        self.k2 = 1.0 / (tau * self._freq)**2.0
        self.k3 = (self._resp * self._damp) / (tau * self._freq)

    def update(self, dt: float, nx: A, dx: Optional[A] = None):
        dx = dx or (nx - self.xp) / dt
        self.xp = nx
        self.y = self.y + self.dy * dt
        self.dy = self.dy + (self.xp + dx * self.k3 - self.y - self.dy * self.k1) * dt / self.k2

        return self.y
