from time import perf_counter_ns
from typing import Callable

import imgui

__all__ = (
    "perf_timed",
    "perf_timed_context",
    "PERF_TRACKER"
)

class PerfTracker:

    def __init__(self):
        self._func_timings: dict[Callable, list] = {}
        self._func_call_count: dict[Callable, int] = {}
        self._contexts: dict[str, set[Callable]] = {"":set()}

    def track_function(self, func: Callable, contexts: tuple[str, ...] = ()):
        if func in self._func_timings:
            raise KeyError("This function is already being tracked")

        self._func_timings[func] = []
        self._func_call_count[func] = 0
        self._contexts[""].add(func)
        for context in contexts:
            context_funcs = self._contexts.get(context, set())
            context_funcs.add(func)
            self._contexts[context] = context_funcs

    def __setitem__(self, func: Callable, elapsed_time: float):
        self._func_timings[func].append(elapsed_time)
        self._func_call_count[func] += 1

    def imgui_draw(self, *contexts):
        for context in contexts:
            expanded, visible = imgui.collapsing_header(f"Function Timings: {context}")

            if expanded:
                for func in self._contexts[context]:
                    count = self._func_call_count[func]
                    if not count:
                        imgui.text(f"{func.__qualname__} - avg: N/A - count: {count}")
                        if imgui.is_item_hovered():
                            imgui.set_tooltip(f"{func}")
                        return
                    timings = self._func_timings[func]
                    avg_count = min(count, 10)
                    avg_timing = sum(timings[-avg_count:]) / avg_count

                    imgui.text(f"{func.__qualname__} - avg: {avg_timing * 1e-6 :.3f}ms - count: {count}")
                    if imgui.is_item_hovered():
                        imgui.set_tooltip(f"{func}")

        imgui.separator()


PERF_TRACKER = PerfTracker()


def perf_timed_context(*contexts):
    def perf_timed(func: Callable):
        PERF_TRACKER.track_function(func, contexts)

        def _count(*args, **kwargs):
            start = perf_counter_ns()
            val = func(*args, **kwargs)
            elapsed = (perf_counter_ns() - start)
            PERF_TRACKER[func] = elapsed
            return val

        return _count

    return perf_timed


def perf_timed(func: Callable):
    PERF_TRACKER.track_function(func)

    def _count(*args, **kwargs):
        start = perf_counter_ns()
        val = func(*args, **kwargs)
        elapsed = (perf_counter_ns() - start)
        PERF_TRACKER[func] = elapsed
        return val

    return _count
