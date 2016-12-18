import unittest
import requests
from mock import MagicMock

from model.querier import Stock
from model.querier import PriceQuerier


response = '{ \
     "query": { \
      "count": 2, \
      "created": "2016-12-18T04:01:15Z", \
      "lang": "en-US", \
      "results": { \
       "quote": [ \
        { \
         "LastTradePriceOnly": "150.00" \
        }, \
        { \
         "LastTradePriceOnly": "90.9" \
        } \
       ] \
      } \
     } \
    }'

error_response = '{ \
     "query": { \
      "count": 1, \
      "created": "2016-12-18T04:01:15Z", \
      "lang": "en-US", \
      "results": { \
       "quote": [ \
        { \
         "LastTradePriceOnly": "150.00" \
        } \
       ] \
      } \
     } \
    }'

status_code = 200

class FakeResponse(object):
    status_code = status_code
    response = response

    @property
    def status_code(self):
        return FakeResponse.status_code

    @property
    def text(self):
        return FakeResponse.response


class PriceQuerierTestCase(unittest.TestCase):
    def setUp(self):
        requests.get = MagicMock(return_value = FakeResponse())


    def test_query(self):
        expected_stocks = [Stock('1565.TWO', 150), Stock('2727.TW', 90.9)]
        FakeResponse.status_code = status_code
        FakeResponse.response = response

        pq = PriceQuerier(requests)
        stocks = pq.query(['1565.TWO', '2727.TW'])
        requests.get.assert_called_with('https://query.yahooapis.com/v1/public/yql?q=select LastTradePriceOnly from yahoo.finance.quote where symbol in ("1565.TWO","2727.TW")&format=json&env=store://datatables.org/alltableswithkeys&callback=')
        self.assertEqual(stocks, expected_stocks)

    def test_query_failed(self):
        FakeResponse.status_code = 500

        pq = PriceQuerier(requests)
        stocks = pq.query(['1565.TWO', '2727.TW'])
        self.assertEqual(len(stocks), 0)

        FakeResponse.status_code = 200
        FakeResponse.response = error_response

        pq = PriceQuerier(requests)
        stocks = pq.query(['1565.TWO', '2727.TW'])
        self.assertEqual(len(stocks), 0)
