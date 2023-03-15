from psutil import Process
import os

from .ddqueue import DataDoubleQueue

class RAMTracer(DataDoubleQueue):
    def __init__(self, process: Process):
        super().__init__(process)

    def measure(self):
        mem_bytes = self.process.memory_info().rss
        self.log(mem_bytes)
        print("Process (current, parent):", os.getpid(), os.getppid())
        print("RAM Measure: {}".format(mem_bytes))

    def collapse(self, start: int, interval: int):
        end = start + interval
        avg = 0
        copy = self.real_time.copy()
        list_len = len(copy)
        for i in range(list_len):
            log = copy[i]
            if log[0] > end:
                break
            
            if i == list_len - 1 or copy[i + 1][0] > end:
                leng = end - log[0]
                avg += log[1] * leng

                self.real_time.pop(0)
                self.real_time.insert(0, (end, log[1]))

            else:
                leng = copy[i + 1][0] - log[0]
                avg += log[1] * leng

                self.real_time.pop(0)
        
        self.aggregate.append((start, interval, avg))
        print("Process (current, parent):", os.getpid(), os.getppid())
        print("RAM Collapse: {}".format(avg))