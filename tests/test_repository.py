# -*- coding: utf-8 -*-

import unittest
import os

from model.repository import StockNameRepository


class NameRepositoryTestCase(unittest.TestCase):
    def test_get_name(self):
        number = '1565.TWO'
        expected_name = u'TICON'

        stock_name_repository = StockNameRepository('./name.db')

        self.assertEqual(stock_name_repository.get_name(number), expected_name)
        self.assertEqual(stock_name_repository.get_name(9999), None)

    def test_save_name(self):
        number = '1565.TWO'
        name = u'TICON'

        stock_name_repository = StockNameRepository('./save_name.db')
        self.assertEqual(stock_name_repository.get_name(number), None)
        stock_name_repository.save_name(number, name)

        self.assertEqual(stock_name_repository.get_name(number), name)

        os.remove('./save_name.db')
