import unittest
import psutil

from otcic.ddqueue import DataDoubleQueue

class TestDataDoubleQueue(unittest.TestCase):
    def setUp(self):
        self.ddq = DataDoubleQueue(psutil.Process())

    def test_len_logged(self):
        for i in range(1000):
            self.ddq.log(123)
        self.assertEqual(1000, len(self.ddq.real_time))
