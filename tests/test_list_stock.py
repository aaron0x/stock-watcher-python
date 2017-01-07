# -*- coding: utf-8 -*-

import unittest
from mock import Mock
from BeautifulSoup import BeautifulSoup

from controller.list import ListStockController
from model.configuration import LogConfig
from model.configuration import WatchCondition


class ListStockControllerTestCase(unittest.TestCase):
    def test_list(self):
        mapper_attrs = {'map_async.return_value': [u'精華', u'王品']}
        mock_name_mapper = Mock(**mapper_attrs)

        watch_condtions = [WatchCondition(u'1565', 0.1, 123.4), WatchCondition(u'2727', 10.0, 88.0)]
        log_setting = LogConfig('ERROR', '/home', 102400, 2)
        config_attrs = {'query_timeout': 3, 'repository_path': './name.db',
                        'log_setting': log_setting, 'watch_conditions': watch_condtions}
        mock_config = Mock(**config_attrs)

        controller = ListStockController(mock_config, mock_name_mapper)
        title = [u'代號', u'名稱', u'買入價', u'賣出價']
        raw1 = [u'1565', u'精華', u'0.1', u'123.4']
        raw2 = [u'2727', u'王品', u'10.0', u'88.0']
        expected_raws = [title, raw1, raw2]

        page = ListPage(controller.list_async(None).result)
        self.assertEqual(page.rows, expected_raws)


class ListPage(object):
    def __init__(self, content):
        self.soup = BeautifulSoup(content)

    @property
    def rows(self):
        data = []
        rows = self.soup.table.findChildren(['tr'])
        for r in rows:
            a_row = [r.string for r in r.findChildren(['th', 'td'])]
            data.append(a_row)
        return data
