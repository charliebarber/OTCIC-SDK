import unittest
import time

from otcic.aggregate import AggregateModel

class TestAggregateModel(unittest.TestCase):
    def setUp(self):
        self.model = AggregateModel(1)

    

    def test_interval_wait(self):
        self.model.measure()
        current = self.model.next_interval
        time.sleep(self.model.interval)
        self.model.measure()
        self.assertEqual(current + self.model.interval, self.model.next_interval)
