import unittest

from model.configuration import WatchCondition
from model.configuration import WatchConfigParser
from model.configuration import SMTPSetting
from model.configuration import LogSetting


class WatchConfigParserTestCase(unittest.TestCase):
    def test_read(self):
        wc1 = WatchCondition('1565.TWO', 0.1, 123.4)
        wc2 = WatchCondition('2727.TW', 10.0, 88.0)
        expected_wcs = [wc1, wc2]
        expected_mails = ['aaron1126@gmail.com', 'silver@yahoo.com']
        expected_smtp_setting = SMTPSetting('smtp.gmail.com:587', 'aaron', 'TWRocks', 'aaron@gmail.com', 'Stock Watcher')
        expected_log_setting = LogSetting('ERROR', '/home', 102400, 2)

        wcp = WatchConfigParser()
        wcp.read("./config")

        self.assertEqual(wcp.watch_conditions, expected_wcs)
        self.assertEqual(wcp.to_addrs, expected_mails)
        self.assertEqual(wcp.smtp_setting, expected_smtp_setting)
        self.assertEqual(wcp.query_timeout, 3)
        self.assertEqual(wcp.log_setting, expected_log_setting)
