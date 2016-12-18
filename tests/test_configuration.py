import unittest

from model.configuration import WatchCondition
from model.configuration import WatchConfigParser


class WatchConfigParserTestCase(unittest.TestCase):
    def test_read(self):
        wc1 = WatchCondition('1565.TWO', 0.1, 123.4)
        wc2 = WatchCondition('2727.TW', 10.0, 88.0)
        expected_wcs = [wc1, wc2]
        expected_mails = ['aaron1126@gmail.com', 'silver@yahoo.com']

        wcp = WatchConfigParser()
        wcp.read("./config")

        self.assertEqual(wcp.watch_conditions, expected_wcs)
        self.assertEqual(wcp.mails, expected_mails)
