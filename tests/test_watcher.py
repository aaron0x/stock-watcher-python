import unittest
from mock import MagicMock
from mock import Mock

from model.configuration import WatchCondition
from model.configuration import SMTPSetting
from model.querier import Stock
from model.watcher import Watcher


class WatcherTestCase(unittest.TestCase):
    def test_watch(self):
        expected_smtp_setting = SMTPSetting('smtp.gmail.com:587', 'aaron', 'TWRocks', 'aaron@gmai.com', 'subject')
        expected_message = '1565.TWO is [150], out of (0.1, 123.4)'
        expected_to_adds = ['aaron1126@gmail.com', 'silver@yahoo.com']

        wc1 = WatchCondition('1565.TWO', 0.1, 123.4)
        wc2 = WatchCondition('2727.TW', 10.0, 88.0)
        watch_config_parser = Mock(watch_conditions = [wc1, wc2], smtp_setting = expected_smtp_setting, to_addrs = expected_to_adds)
        attrs = {'query.return_value' : [Stock('1565.TWO', 150), Stock('2727.TW', 50.9)]}
        price_querier = Mock(**attrs)
        notifier = MagicMock()


        w = Watcher(watch_config_parser, price_querier, notifier)
        w.watch('./config')

        notifier.notify.assert_called_with(expected_smtp_setting ,expected_to_adds, expected_message)
