import unittest

from model.configuration import WatchCondition
from model.configuration import WatchConfigParser


class WatchConfigParserTestCase(unittest.TestCase):
    def test_read(self):
        wc1 = WatchCondition('1565.TWO', 0.1, 123.4)
        wc2 = WatchCondition('2727.TW', 10.0, 88.0)
        expected_wcs = [wc1, wc2]

        wcp = WatchConfigParser()
        wcs = wcp.read("./config")

        self.assertEqual(wcs, expected_wcs)
