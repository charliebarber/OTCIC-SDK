import tracemalloc

from ddqueue import DataDoubleQueue

if not tracemalloc.is_tracing():
    tracemalloc.start()

class RAMTracer(DataDoubleQueue):
    def __init__(self):
        super().__init__()

    def measure(self):
        mem_bytes, _ = tracemalloc.get_traced_memory()
        self.log(mem_bytes)

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