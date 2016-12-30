# -*- coding: utf-8 -*-

import unittest
from BeautifulSoup import BeautifulSoup

from controller.list import ListStockController


class ListStockControllerTestCase(unittest.TestCase):
    def test_list(self):
        controller = ListStockController('./config')
        title = [u'Number', u'Buy', u'Sell']
        raw1 = [u'1565.TWO', u'0.1', u'123.4']
        raw2 = [u'2727.TW', u'10.0', u'88.0']
        expected_raws = [title, raw1, raw2]

        page = ListPage(controller.list())
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
