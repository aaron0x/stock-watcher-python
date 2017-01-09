# -*- coding: utf-8 -*-

import unittest
from mock import Mock

from model.name_map import NameMapper


class StockNameMapperTestCase(unittest.TestCase):
    def test_map_from_repository(self):
        numbers = [u'1565.TWO']
        expected_names = [u'精華']
        attrs = {'get_name.return_value': u'精華'}
        repository = Mock(**attrs)
        name_querier = Mock()

        mapper = NameMapper(repository, name_querier)
        result = mapper.map_async(numbers, 3)

        self.assertEqual(result.result, expected_names)
        repository.get_name.assert_called_once()
        name_querier.assert_not_called()

    def test_map_from_querier(self):
        numbers = [u'1565.TWO']
        expected_names = [u'精華']
        attrs1 = {'get_name.return_value': None}
        repository = Mock(**attrs1)
        attrs2 = {'query_async.return_value': u'精華'}
        name_querier = Mock(**attrs2)

        mapper = NameMapper(repository, name_querier)
        result = mapper.map_async(numbers, 3)

        self.assertEqual(result.result, expected_names)
        repository.get_name.assert_called_once()
        name_querier.query_async.assert_called_once()
        repository.save_name.assert_called_with(u'1565.TWO', u'精華')

