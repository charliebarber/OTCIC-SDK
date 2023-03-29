import unittest
import psutil
import time

from otcic.cpu_tracer import CPUTracer

cpu_cores = psutil.cpu_count()

class TestCPUTracer(unittest.TestCase):
    def setUp(self):
        self.tracer = CPUTracer(psutil.Process())

    def test_cpu_usage_sanity(self):
        self.tracer.collapse(0, 1)
        time.sleep(1)
        self.tracer.collapse(1, 1)
        value = self.tracer.aggregate.pop()[2]
        self.assertGreaterEqual(value, 0)
        self.assertLessEqual(value, cpu_cores * 1.5)
