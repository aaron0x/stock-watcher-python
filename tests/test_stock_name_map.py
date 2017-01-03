# -*- coding: utf-8 -*-

import unittest
from mock import Mock

from model.stock_name_map import StockNameMapper


class StockNameMapperTestCase(unittest.TestCase):
    def test_map_from_repository(self):
        stock_numbers = ['1565.TWO']
        expected_names = [u'精華']
        attrs = {'name.return_value': u'精華'}
        repository = Mock(**attrs)
        name_querier = Mock()

        mapper = StockNameMapper(repository, name_querier)
        result = mapper.map_async(stock_numbers)

        name_querier.assert_not_called()
        repository.name.assert_called_once()
        self.assertEqual(expected_names, result.result)

    def test_map_from_querier(self):
        stock_numbers = ['1565.TWO']
        expected_names = [u'精華']
        attrs1 = {'name.return_value': None}
        repository = Mock(**attrs1)
        attrs2 = {'query.return_value': u'精華'}
        name_querier = Mock(**attrs2)

        mapper = StockNameMapper(repository, name_querier)
        result = mapper.map_async(stock_numbers)

        repository.name.assert_called_once()
        repository.save.assert_called_with('1565.TWO', u'精華')
        name_querier.query.assert_called_once()
        self.assertEqual(expected_names, result.result)
