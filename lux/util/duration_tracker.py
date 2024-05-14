from dataclasses import dataclass, field
from time import perf_counter_ns
from typing import Callable

import imgui

__all__ = (
    "perf_timed",
    "perf_timed_context",
    "PERF_TRACKER"
)

@dataclass(slots=True)
class FuncTracker:
    timings: list[float] = field(default_factory=list)
    count: int = 0
    update_count: int = 0
    update_elapsed: float = 0.0
    update_count_history: list[int] = field(default_factory=list)
    update_elapsed_history: list[float] = field(default_factory=list)
    contexts: set[str] = field(default_factory=lambda: {""})


class PerfTracker:

    def __init__(self):
        self._funcs: dict[Callable, FuncTracker] = {}
        self._contexts: dict[str, set[Callable]] = {"": set()}

    def track_function(self, func: Callable, contexts: tuple[str, ...] = ()):
        if func in self._funcs:
            raise KeyError("This function is already being tracked")

        tracker = FuncTracker()
        self._funcs[func] = tracker
        self._contexts[""].add(func)
        for context in contexts:
            tracker.contexts.add(context)
            context_set = self._contexts.get(context, set())
            context_set.add(func)
            self._contexts[context] = context_set

    def __setitem__(self, func: Callable, elapsed_time: float):
        tracker = self._funcs[func]
        tracker.timings.append(elapsed_time)
        tracker.update_elapsed += elapsed_time
        tracker.count += 1
        tracker.update_count += 1

    def cache_update(self):
        for tracker in self._funcs.values():
            tracker.update_count_history.append(tracker.update_count)
            tracker.update_elapsed_history.append(tracker.update_elapsed)
            tracker.update_count = 0
            tracker.update_elapsed = 0.0

    def imgui_draw(self, *contexts):
        for context in contexts:
            expanded, visible = imgui.collapsing_header(f"Function Timings: {context}")

            if expanded:
                for func in self._contexts[context]:
                    if imgui.is_item_hovered():
                        imgui.set_tooltip(f"{func}")
                    tracker = self._funcs[func]
                    if not tracker.count:
                        imgui.text(f"{func.__qualname__} - Uncalled")
                        return
                    timings = tracker.timings
                    avg_count = min(tracker.count, 10)
                    avg_timing = sum(timings[-avg_count:]) / avg_count

                    update_counts = tracker.update_count_history
                    update_elapsed = tracker.update_elapsed_history
                    update_count = min(len(update_counts), 10)

                    if not update_count:
                        imgui.text(f"{func.__qualname__} - avg: {avg_timing * 1e-6 :.3f}ms - count: {tracker.count}")
                        return

                    avg_counts = int(sum(update_counts[-update_count:]) / update_count)
                    avg_elapsed = sum(update_elapsed[-update_count:]) / update_count

                    imgui.text(f"{func.__qualname__} - avg: {avg_timing * 1e-6 :.3f}ms - count: {tracker.count} - avg update elapsed: {avg_elapsed * 1e-6 :.3f} - avg call count: {avg_counts}")


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
    PERF_TRACKER.track_function(func, (func.__name__,))

    def _count(*args, **kwargs):
        start = perf_counter_ns()
        val = func(*args, **kwargs)
        elapsed = (perf_counter_ns() - start)
        PERF_TRACKER[func] = elapsed
        return val

    return _count
