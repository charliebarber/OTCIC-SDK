import time
from psutil import Process

from .ddqueue import DataDoubleQueue

class CPUTracer(DataDoubleQueue):
    def __init__(self, process: Process):
        super().__init__(process)
        self.last_time = time.monotonic()
        self.last_proc = self.process.cpu_times().user

    def collapse(self, start: int, interval: int):
        new_time = time.monotonic()
        new_proc = self.process.cpu_times().user

        self.aggregate.append((start, interval, (new_proc - self.last_proc) / (new_time - self.last_time)))

        self.last_time = new_time
        self.last_proc = new_proc