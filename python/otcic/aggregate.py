import time

from ddqueue import DataDoubleQueue
from cpu_tracer import CPUTracer
from ram_tracer import RAMTracer
from disk_tracer import DiskTracer
from gpu_tracer import GPUTracer

class AggregateModel:
    def __init__(self, interval: int):
        self.interval = interval
        self.next_interval = int(time.time() // interval) * interval
        self.tracers: dict[str, DataDoubleQueue] = {
            "cpu": CPUTracer(),
            "ram": RAMTracer(),
            "disk": DiskTracer(),
            "gpu": GPUTracer()
        }

    def measure(self):
        tracer_values = self.tracers.values()
        for tracer in tracer_values:
            tracer.measure()
        
        if time.time() > self.next_interval:
            start = self.next_interval - self.interval
            for tracer in tracer_values:
                tracer.collapse(start, self.interval)

    def get_metrics(self):
        return [values.aggregate for values in self.tracers.values()]
