from time import perf_counter_ns
from typing import Callable

from pyglet.math import Vec2

import imgui

__all__ = (
    "perf_timed",
    "PERF_TRACKER"
)

class PerfTracker:

    def __init__(self):
        self._func_timings: dict[Callable, list] = {}
        self._func_call_count: dict[Callable, int] = {}

    def track_function(self, func: Callable):
        if func in self._func_timings:
            raise KeyError("This function is already being tracked")

        self._func_timings[func] = []
        self._func_call_count[func] = 0

    def __setitem__(self, func: Callable, elapsed_time: float):
        self._func_timings[func].append(elapsed_time)
        self._func_call_count[func] += 1

    def imgui_draw(self):
        imgui.separator()
        imgui.text_wrapped("Function Timings")

        for func in self._func_timings:
            count = self._func_call_count[func]
            if not count:
                imgui.text(f"{func.__name__} - avg: N/A - count: {count}")
                continue
            timings = self._func_timings[func]
            avg_count = min(count, 10)
            avg_timing = sum(timings[-avg_count:]) / avg_count

            imgui.text(f"{func.__name__} - avg: {avg_timing * 1e-6 :.3f}ms - count: {count}")

        imgui.separator()


PERF_TRACKER = PerfTracker()


def perf_timed(func: Callable):
    PERF_TRACKER.track_function(func)

    def _count(*args, **kwargs):
        start = perf_counter_ns()
        func(*args, **kwargs)
        elapsed = (perf_counter_ns() - start)
        PERF_TRACKER[func] = elapsed

    return _count
