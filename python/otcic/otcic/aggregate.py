import time
from psutil import Process
from typing import Any

from .ddqueue import DataDoubleQueue
from .cpu_tracer import CPUTracer
from .ram_tracer import RAMTracer
from .disk_tracer import DiskTracer
from .gpu_tracer import GPUTracer, VRAMTracer

import os

class AggregateModel:
    def __init__(self, interval: int):
        self.interval = interval
        self.process = Process()
        self.next_interval = int(time.time() // interval) * interval
        self.tracers: dict[str, DataDoubleQueue] = {
            "cpu": CPUTracer(self.process),
            "ram": RAMTracer(self.process),
            "disk": DiskTracer(self.process),
            "gpu": GPUTracer(self.process),
            "vram": VRAMTracer(self.process)
        }
        self.lock = False
        print("Aggr creation, pid:", self.process.pid)

    def measure(self):
        if self.lock:
            return

        self.lock = True

        #print("Aggr Process (curr,par): {:>4} | {:>4}".format(os.getpid(), os.getppid()))

        tracer_values = self.tracers.values()
        for tracer in tracer_values:
            tracer.measure()
        
        if time.time() > self.next_interval:
            start = self.next_interval - self.interval
            for tracer in tracer_values:
                tracer.collapse(start, self.interval)
            self.next_interval = self.next_interval + self.interval

        self.lock = False

    def get_metrics(self) -> dict[str, list[tuple[int, int, Any]]]:
        return {key: values.aggregate for key, values in self.tracers.items()}
