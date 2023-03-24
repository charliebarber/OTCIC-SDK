import unittest
import random as r

from .generate_data import generate_real_time_list
from otcic import utils



class CAData:
    def __init__(self):
        self.start = r.randint(1, 30)
        self.interval = 3
        self.data = generate_real_time_list(self.start)
        self.value, self.newdata = utils.collapse_avg(self.data, self.start, self.interval)

def generate_CAData_log(start, interval, data):
    return "\n".join([
        "\nStart: {}".format(start),
        "Interval: {}".format(interval),
        "Real Time List:"
    ] + [
        "{}".format(item) for item in data
    ])



# single real_time list
class TestCollapseAvgA(unittest.TestCase):
    def setUp(self):
        self.data = [CAData() for i in range(1000)]

    def test_time_interval(self):
        for item in self.data:
            self.assertAlmostEqual(item.start + item.interval, item.newdata[0][0], 3)
    
    def test_item_count(self):
        for item in self.data:
            initial_count = len(item.data)
            final_count = len(item.newdata)
            removed_count = len([
                None
                for i in item.data
                if i[0] < item.start + item.interval
            ]) - 1
            self.assertEqual(initial_count - final_count, removed_count)
    
    def test_average_value(self):
        for item in self.data:
            avg = sum([
                item.data[i][1] * (min(
                    item.data[i+1][0], item.start + item.interval
                ) - item.data[i][0])
                for i in range(len(item.data) - 1)
                if item.data[i][0] < item.start + item.interval
            ]) / item.interval
            self.assertAlmostEqual(avg, item.value, 3)

# merging multiple real time lists
class TestCollapseAvgB(unittest.TestCase):
    def setUp(self):
        self.start = 0
        self.interval = 3
        self.data = [generate_real_time_list(0, self.interval * 3) for i in range(1000)]

    def test_avg(self):
        for data in self.data:
            merged_avgs = []
            data_copy = data.copy()
            for i in range(3):
                avg, newdata = utils.collapse_avg(data_copy, self.start + self.interval * i, self.interval)
                merged_avgs.append(avg)
                data_copy.clear()
                data_copy.extend(newdata)

            normal_avg = utils.collapse_avg(data, self.start, self.interval * 3)[0]
            self.assertAlmostEqual(
                sum(merged_avgs) / 3,
                normal_avg,
                3,
                "".join([
                    "\nMerged averages: {}\n".format(merged_avgs),
                    generate_CAData_log(self.start, self.interval, data)
                ])
            )