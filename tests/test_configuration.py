import unittest

from model.configuration import WatchCondition
from model.configuration import WatchConditionParser
from model.configuration import LogSettingParser
from model.configuration import WatchConfigParser
from model.configuration import SMTPSetting
from model.configuration import LogSetting
from model.configuration import DBConfigParser
from model.configuration import WebConfig


class WatchCoditionParserTestCase(unittest.TestCase):
    def test_parse(self):
        wc1 = WatchCondition('1565.TWO', 0.1, 123.4)
        wc2 = WatchCondition('2727.TW', 10.0, 88.0)
        expected_wcs = [wc1, wc2]

        parser = WatchConditionParser()
        parser.parse('./config')

        self.assertEqual(parser.watch_conditions, expected_wcs)


class LogSettingParserTestCase(unittest.TestCase):
    def test_parse(self):
        expected_log_setting = LogSetting('ERROR', '/home', 102400, 2)

        parser = LogSettingParser()
        parser.parse('./config')

        self.assertEqual(parser.log_setting, expected_log_setting)


class WatchConfigParserTestCase(unittest.TestCase):
    def test_parse(self):
        wc1 = WatchCondition('1565.TWO', 0.1, 123.4)
        wc2 = WatchCondition('2727.TW', 10.0, 88.0)
        expected_wcs = [wc1, wc2]
        expected_mails = ['aaron1126@gmail.com', 'silver@yahoo.com']
        expected_smtp_setting = SMTPSetting('smtp.gmail.com:587', 'aaron', 'TWRocks', 'aaron@gmail.com', 'Stock Watcher')
        expected_log_setting = LogSetting('ERROR', '/home', 102400, 2)

        wcp = WatchConfigParser()
        wcp.parse("./config")

        self.assertEqual(wcp.watch_conditions, expected_wcs)
        self.assertEqual(wcp.to_addrs, expected_mails)
        self.assertEqual(wcp.smtp_setting, expected_smtp_setting)
        self.assertEqual(wcp.query_timeout, 3)
        self.assertEqual(wcp.log_setting, expected_log_setting)


class WebConfigTestCase(unittest.TestCase):
    def test_read(self):
        wc1 = WatchCondition('1565.TWO', 0.1, 123.4)
        wc2 = WatchCondition('2727.TW', 10.0, 88.0)
        expected_wcs = [wc1, wc2]
        expected_log_setting = LogSetting('ERROR', '/home', 102400, 2)

        config = WebConfig()
        config.read("./config")

        self.assertEqual(config.watch_conditions, expected_wcs)
        self.assertEqual(config.query_timeout, 3)
        self.assertEqual(config.log_setting, expected_log_setting)
        self.assertEqual(config.db_path, '/home')


class DBConfigParserTestCase(unittest.TestCase):
    def test_parse(self):
        expected_path = '/home'

        parser = DBConfigParser()
        parser.parse("./config")

        self.assertEqual(parser.path, expected_path)
