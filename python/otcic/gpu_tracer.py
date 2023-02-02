from psutil import Process
import gpustat
from gpustat import GPUStat

from ddqueue import DataDoubleQueue

# NVIDIA compatible only!
class GPUTracer(DataDoubleQueue):
    def __init__(self, process: Process):
        super().__init__(process)

    def measure(self):
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