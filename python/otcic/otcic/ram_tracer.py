from psutil import Process
import os

from .ddqueue import DataDoubleQueue
from .utils import collapse_avg

class RAMTracer(DataDoubleQueue):
    def __init__(self, process: Process):
        super().__init__(process)

    def measure(self):
        mem_bytes = self.process.memory_info().rss
        self.log(mem_bytes)
        #print("Process (curr,par): {:>4} | {:>4} | RAM Measure: {}".format(os.getpid(), os.getppid(), mem_bytes))

    def collapse(self, start: int, interval: int):
        avg, self.real_time = collapse_avg(self.real_time, start, interval)
        self.aggregate.append((start, interval, avg))
        print("Process (curr,par): {:>4} | {:>4} | RAM Collapse: {}".format(os.getpid(), os.getppid(), avg))