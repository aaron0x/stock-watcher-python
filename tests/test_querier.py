import unittest
import treq
import json
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
    def code(self):
        return FakeResponse.status_code

    def json(self):
        return json.loads(FakeResponse.response)


class PriceQuerierTestCase(unittest.TestCase):
    def setUp(self):
        self.org_get = treq.get
        treq.get = MagicMock(return_value = FakeResponse())

    def tearDown(self):
        treq.get = self.org_get

    def test_query(self):
        expected_stocks = [Stock('1565.TWO', 150), Stock('2727.TW', 90.9)]
        FakeResponse.status_code = status_code
        FakeResponse.response = response

        pq = PriceQuerier(treq)
        d = pq.query_async(['1565.TWO', '2727.TW'])
        treq.get.assert_called_with('https://query.yahooapis.com/v1/public/yql?q=select%20LastTradePriceOnly%20from%20yahoo.finance.quote%20where%20symbol%20in%20(%221565.TWO%22%2C%222727.TW%22)&format=json&env=store%3A//datatables.org/alltableswithkeys&callback=')
        self.assertEqual(d.result, expected_stocks)

    def test_query_failed(self):
        FakeResponse.status_code = 500

        pq = PriceQuerier(treq)
        d = pq.query_async(['1565.TWO', '2727.TW'])
        self.assertEqual(len(d.result), 0)

        FakeResponse.status_code = 200
        FakeResponse.response = error_response

        pq = PriceQuerier(treq)
        d = pq.query_async(['1565.TWO', '2727.TW'])
        self.assertEqual(len(d.result), 0)


# class PriceQuerierTestCase1(unittest.TestCase):
#     def test_real_query(self):
#         from twisted.internet import reactor
#
#         pq = PriceQuerier(treq)
#         r = pq.query_async(['1565.TWO', '2727.TW'])
#         reactor.callLater(2, reactor.stop)
#         reactor.run()
#         print r

