import time
from psutil import Process
import gpustat
from gpustat import GPUStat

from .ddqueue import DataDoubleQueue
from .utils import collapse_avg

def get_gpu_process(pid: int):
    gpu_processes = []
    gpu_collection = gpustat.new_query()
    gpu_list: list[GPUStat] = gpu_collection.gpus
    for gpu in gpu_list:
        for process in gpu.processes:
            if process["pid"] == pid:
                gpu_processes.append(process)
    return gpu_processes

class GPUTracer(DataDoubleQueue):
    def __init__(self, process: Process):
        super().__init__(process)
        self.warned = False

    def collapse(self, start: int, interval: int):
        try:
            gpu_averages = [(gpu.utilization or 0) for gpu in gpustat.new_query().gpus]
            gpu_average = sum(gpu_averages) / len(gpu_averages)

        except Exception as e:
            gpu_average = 0

            if not self.warned:
                self.warned = True
                print("Unsupported GPU, not using NVIDIA, can't measure GPU usage")
                print(e)

        self.aggregate.append((start, interval, gpu_average))
        #print("GPU Collapse: {}".format(gpu_average))

class VRAMTracer(DataDoubleQueue):
    def __init__(self, process: Process):
        super().__init__(process)
        self.warned = False

    def measure(self):
        try:
            gpu_processes = get_gpu_process(self.process.pid)
            memory = sum([(process["gpu_memory_usage"] or 0) for process in gpu_processes])

        except Exception as e:
            memory = 0

            if not self.warned:
                self.warned = True
                print("Unsupported GPU, not using NVIDIA, can't measure VRAM")
                print(e)
        
        self.log(memory)

    def collapse(self, start: int, interval: int):
        avg, self.real_time = collapse_avg(self.real_time, start, interval)
        self.aggregate.append((start, interval, avg))
        #print("VRAM Collapse: {}".format(avg))