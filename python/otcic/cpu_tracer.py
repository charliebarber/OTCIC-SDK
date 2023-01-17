import time

from ddqueue import DataDoubleQueue

class CPUTracer(DataDoubleQueue):
    def __init__(self):
        super().__init__()
        self.last_time = time.monotonic_ns()
        self.last_proc = time.process_time_ns()
    
    def measure(self):
        cur_time = time.monotonic_ns()
        cur_proc = time.process_time_ns()

        self.log([cur_proc - self.last_proc, cur_time - self.last_time])

        self.last_time = cur_time
        self.last_proc = cur_proc

    def collapse(self, start: int, interval: int):
        end = start + interval
        copy = self.real_time.copy()
        list_len = len(copy)

        total_time = 1 #0
        total_proc = 0

#        for i in range(list_len):
#            log = copy[i]
#            if log[0] > end:
#                total_time = 1
#                break

        self.aggregate.append((start, interval, total_proc / total_time))