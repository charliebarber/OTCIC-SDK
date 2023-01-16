import time
from typing import Any

# 2 queues:
# - aggergate queue
# - real time queue
# consider putting this to server-side processing?
TIME_INTERVAL = 30

class DataDoubleQueue:
    def __init__(self):
        self.aggregate = []
        self.real_time: list[tuple[float, Any]] = []

    def log(self, entry):
        entry_time = time.time()
        self.real_time.append((entry_time, entry))
