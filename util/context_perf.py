from logging import getLogger
from time import perf_counter_ns


class LogSection:
    def __init__(self, name: str = "perf counter", logger: str = "lux"):
        self.logger = getLogger(logger)
        self.name = name
        self.start_time = -1.0

    def done(self):
        duration = (perf_counter_ns() - self.start_time) / 1e6
        self.logger.debug(f"Done {self.name} ({duration:.3f}ms)")

    def __enter__(self):
        self.logger.debug(f"Starting {self.name}")
        self.start_time = perf_counter_ns()

    def __exit__(self, type, value, traceback):
        if type is None:
            self.done()