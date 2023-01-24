import time

from ddqueue import DataDoubleQueue

class CPUTracer(DataDoubleQueue):
    def __init__(self):
        super().__init__()
        self.last_time = time.monotonic_ns()
        self.last_proc = time.process_time_ns()

    def collapse(self, start: int, interval: int):
        new_time = time.monotonic_ns()
        new_proc = time.process_time_ns()

        self.aggregate.append((start, interval, new_proc / new_time))

        self.last_time = new_time
        self.last_proc = new_proc