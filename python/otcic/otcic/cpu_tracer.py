import time
import psutil
Process = psutil.Process
core_mult = (1 / psutil.cpu_count()) * 0.01

from .ddqueue import DataDoubleQueue

class CPUTracer(DataDoubleQueue):
    def __init__(self, process: Process):
        super().__init__(process)
        self.process.cpu_percent()

    def collapse(self, start: int, interval: int):
        cpu_usage = self.process.cpu_percent() * core_mult
        self.aggregate.append((start, interval, cpu_usage))
