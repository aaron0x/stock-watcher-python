import unittest
import codecs
from ConfigParser import ConfigParser

from model.configuration import WatchCondition
from model.configuration import WatchConditionParser
from model.configuration import LogConfigParser
from model.configuration import WatchConfigParser
from model.configuration import SMTPConfig
from model.configuration import LogConfig
from model.configuration import DBConfigParser
from model.configuration import WebConfigParser


class WatchCoditionParserTestCase(unittest.TestCase):
    def test_parse(self):
        wc1 = WatchCondition('1565.TWO', 0.1, 123.4)
        wc2 = WatchCondition('2727.TW', 10.0, 88.0)
        expected_wcs = [wc1, wc2]

        with codecs.open('./config', 'r', 'utf-8') as f:
            c = ConfigParser()
            c.readfp(f)
            parser = WatchConditionParser()
            parser.parse(c)

        self.assertEqual(parser.watch_conditions, expected_wcs)


class LogConfigTestCase(unittest.TestCase):
    def test_parse(self):
        expected_log_config = LogConfig('ERROR', '/home', 102400, 2)

        with codecs.open('./config', 'r', 'utf-8') as f:
            c = ConfigParser()
            c.readfp(f)
            config = LogConfigParser()
            config.parse(c)

        self.assertEqual(config.log_config, expected_log_config)


class WatchConfigParserTestCase(unittest.TestCase):
    def test_parse(self):
        wc1 = WatchCondition('1565.TWO', 0.1, 123.4)
        wc2 = WatchCondition('2727.TW', 10.0, 88.0)
        expected_wcs = [wc1, wc2]
        expected_mails = ['aaron1126@gmail.com', 'silver@yahoo.com']
        expected_smtp_config = SMTPConfig('smtp.gmail.com:587', 'aaron', 'TWRocks', 'aaron@gmail.com', 'Stock Watcher')
        expected_log_config = LogConfig('ERROR', '/home', 102400, 2)

        with codecs.open('./config', 'r', 'utf-8') as f:
            c = ConfigParser()
            c.readfp(f)
            parser = WatchConfigParser()
            parser.parse(c)

        self.assertEqual(parser.watch_conditions, expected_wcs)
        self.assertEqual(parser.to_addrs, expected_mails)
        self.assertEqual(parser.smtp_config, expected_smtp_config)
        self.assertEqual(parser.query_timeout, 3)
        self.assertEqual(parser.log_config, expected_log_config)


class WebConfigParserTestCase(unittest.TestCase):
    def test_parse(self):
        wc1 = WatchCondition('1565.TWO', 0.1, 123.4)
        wc2 = WatchCondition('2727.TW', 10.0, 88.0)
        expected_wcs = [wc1, wc2]
        expected_log_config = LogConfig('ERROR', '/home', 102400, 2)

        with codecs.open('./config', 'r', 'utf-8') as f:
            c = ConfigParser()
            c.readfp(f)
            config = WebConfigParser()
            config.parse(c)

        self.assertEqual(config.watch_conditions, expected_wcs)
        self.assertEqual(config.query_timeout, 3)
        self.assertEqual(config.log_config, expected_log_config)
        self.assertEqual(config.db_path, '/home')


class DBConfigParserTestCase(unittest.TestCase):
    def test_parse(self):
        expected_path = '/home'

        with codecs.open('./config', 'r', 'utf-8') as f:
            c = ConfigParser()
            c.readfp(f)
            parser = DBConfigParser()
            parser.parse(c)

        self.assertEqual(parser.path, expected_path)
