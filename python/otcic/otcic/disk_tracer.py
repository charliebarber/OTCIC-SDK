import time
from psutil import Process
from .ddqueue import DataDoubleQueue
from typing import NamedTuple

class ReadWriteBytes(NamedTuple):
    read: int
    write: int

class DiskTracer(DataDoubleQueue):
    def __init__(self, process: Process):
        super().__init__(process)
        counters = self.process.io_counters()
        self.last_read: int = counters.read_bytes
        self.last_write: int = counters.write_bytes

    def collapse(self, start: int, interval: int):
        counters = self.process.io_counters()
        new_read: int = counters.read_bytes
        new_write: int = counters.write_bytes

        read_write = ReadWriteBytes(new_read - self.last_read, new_write - self.last_write)
        self.aggregate.append((start, interval, read_write))

        self.last_read = new_read
        self.last_write = new_write
