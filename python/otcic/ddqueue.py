import time
from psutil import Process
from typing import Any

# 2 queues:
# - aggergate queue
# - real time queue
# consider putting this to server-side processing?

class DataDoubleQueue:
    def __init__(self, process: Process):
        self.process: Process = process
        self.aggregate: list[tuple[int, int, Any]] = []
        self.real_time: list[tuple[float, Any]] = []

    def log(self, entry: Any):
        entry_time = time.time()
        self.real_time.append((entry_time, entry))

    def measure(self):
        pass

    def collapse(self, start: int, interval: int):
        pass
