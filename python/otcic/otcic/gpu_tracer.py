from psutil import Process
import gpustat
from gpustat import GPUStat

from .ddqueue import DataDoubleQueue

class GPUTracer(DataDoubleQueue):
    def __init__(self, process: Process):
        super().__init__(process)

    def measure(self):
        try:
            gpu_collection = gpustat.new_query()
            process_gpus = []
            gpu_list: list[GPUStat] = gpu_collection.gpus
            for gpu in gpu_list:
                for process in gpu.processes:
                    if process["pid"] == self.process.pid:
                        process_gpus.append(process)
        
            # incomplete and unsafe - need to do sanity check for "None"
            memory = 0
            for process_gpu in process_gpus:
                memory += process_gpu["gpu_memory_usage"]

            # add GPU usage? only cpu usage seen in docs and code

            self.log(memory)
        except Exception as e:
            print("Unsupported GPU, use NVIDIA, returning 0")
            print(e)
            self.log(0)

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