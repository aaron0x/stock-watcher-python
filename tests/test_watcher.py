import unittest
import requests
from mock import MagicMock

from model.configuration import WatchCondition
from model.querier import Stock
from model.watcher import Watcher
from test_querier import FakeResponse


class FakeWatchConfigParser(object):
    def __init__(self):
        wc1 = WatchCondition('1565.TWO', 0.1, 123.4)
        wc2 = WatchCondition('2727.TW', 10.0, 88.0)
        self.watch_conditions = [wc1, wc2]

    def read(self, path):
        pass


class FakePriceQuerier(object):
    def __init__(self, request):
        pass

    def query(self, stock_numbers):
        return [Stock('1565.TWO', 150), Stock('2727.TW', 50.9)]


class FakeNotifier(object):
    message = ''

    def notify(self, SMTPInfo, message):
        FakeNotifier.message = message


class WatcherTestCase(unittest.TestCase):
    def test_watch(self):
        expected_message = '1565.TWO is [150], out of (0.1, 123.4)'
        requests.get = MagicMock(return_value = FakeResponse())

        w = Watcher(FakeWatchConfigParser(), FakePriceQuerier(requests), FakeNotifier())
        w.watch('./config')

        self.assertEqual(FakeNotifier.message, expected_message)
