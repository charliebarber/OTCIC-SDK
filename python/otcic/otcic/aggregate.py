import time
from psutil import Process
from typing import Any

from .ddqueue import DataDoubleQueue
from .cpu_tracer import CPUTracer
from .ram_tracer import RAMTracer
from .disk_tracer import DiskTracer
from .gpu_tracer import GPUTracer

class AggregateModel:
    def __init__(self, interval: int):
        self.interval = interval
        self.process = Process()
        self.next_interval = int(time.time() // interval) * interval
        self.tracers: dict[str, DataDoubleQueue] = {
            "cpu": CPUTracer(self.process),
            "ram": RAMTracer(self.process),
            "disk": DiskTracer(self.process),
            "gpu": GPUTracer(self.process)
        }

    def measure(self):
        tracer_values = self.tracers.values()
        for tracer in tracer_values:
            tracer.measure()
        
        if time.time() > self.next_interval:
            start = self.next_interval - self.interval
            for tracer in tracer_values:
                tracer.collapse(start, self.interval)

    def get_metrics(self) -> dict[str, list[tuple[int, int, Any]]]:
        return {key: values.aggregate for key, values in self.tracers.items()}
