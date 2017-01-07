# -*- coding: utf-8 -*-

import unittest
from mock import Mock

from model.stock_name_map import StockNameMapper


class StockNameMapperTestCase(unittest.TestCase):
    def test_map_from_repository(self):
        stock_numbers = [u'1565.TWO']
        expected_names = [u'精華']
        attrs = {'get_name.return_value': u'精華'}
        repository = Mock(**attrs)
        name_querier = Mock()

        mapper = StockNameMapper(repository, name_querier)
        result = mapper.map_async(stock_numbers, 3)

        name_querier.assert_not_called()
        repository.get_name.assert_called_once()
        self.assertEqual(expected_names, result.result)

    def test_map_from_querier(self):
        stock_numbers = [u'1565.TWO']
        expected_names = [u'精華']
        attrs1 = {'get_name.return_value': None}
        repository = Mock(**attrs1)
        attrs2 = {'query_async.return_value': u'精華'}
        name_querier = Mock(**attrs2)

        mapper = StockNameMapper(repository, name_querier)
        result = mapper.map_async(stock_numbers, 3)

        repository.get_name.assert_called_once()
        repository.save_name.assert_called_with(u'1565.TWO', u'精華')
        name_querier.query_async.assert_called_once()
        self.assertEqual(expected_names, result.result)
