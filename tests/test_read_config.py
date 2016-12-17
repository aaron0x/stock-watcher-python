import unittest

from model.configuration import WatchCondition
from model.configuration import WatchConfigParser


class StockConfigParserTest(unittest.TestCase):
    def test_read_config(self):
        wc1 = WatchCondition('1565', 0.1, 123.4)
        wc2 = WatchCondition('2727', 10.0, 88.0)
        expected_wcs = [wc1, wc2]

        wcp = WatchConfigParser()
        wcs = wcp.read("./config")

        self.assertEqual(wcs, expected_wcs)
