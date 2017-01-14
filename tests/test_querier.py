# -*- coding: utf-8 -*-

import treq
import requests
import json
from mock import MagicMock, Mock, call

from twisted.trial import unittest
from twisted.internet.defer import succeed, fail

from model.querier import Stock, NameQuerier, PriceQuerier, NameQueryRetry, NameQueryException


successful_response = '{ \
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


class FakeResponse(object):
    status_code = 200
    response = successful_response

    @property
    def code(self):
        return FakeResponse.status_code

    def json(self):
        return json.loads(FakeResponse.response)

    def text(self):
        return self.response


class PriceQuerierTestCase(unittest.TestCase):
    def setUp(self):
        self.treq_get = treq.get
        treq.get = MagicMock(return_value = FakeResponse())
        self.requests_get = requests.get
        requests.get = MagicMock(return_value = FakeResponse())

    def tearDown(self):
        treq.get = self.treq_get
        requests.get = self.requests_get

    def test_query(self):
        expected_stocks = [Stock('1565.TWO', 150), Stock('2727.TW', 90.9)]
        FakeResponse.status_code = 200
        FakeResponse.response = successful_response

        pq = PriceQuerier(requests)
        stocks = pq.query(['1565.TWO', '2727.TW'], 3)
        requests.get.assert_called_with('https://query.yahooapis.com/v1/public/yql?q=select%20LastTradePriceOnly%20from%20yahoo.finance.quote%20where%20symbol%20in%20(%221565.TWO%22%2C%222727.TW%22)&format=json&env=store%3A//datatables.org/alltableswithkeys&callback=', timeout = 3)
        self.assertEqual(stocks, expected_stocks)

    def test_query_failed(self):
        FakeResponse.status_code = 500
        FakeResponse.response = successful_response

        pq = PriceQuerier(requests)
        stocks = pq.query(['1565.TWO', '2727.TW'], 3)
        self.assertEqual(stocks, [])

    def test_query_async(self):
        expected_stocks = [Stock('1565.TWO', 150), Stock('2727.TW', 90.9)]
        FakeResponse.status_code = 200
        FakeResponse.response = successful_response

        pq = PriceQuerier(treq)
        d = pq.query_async(['1565.TWO', '2727.TW'], 3)
        treq.get.assert_called_with('https://query.yahooapis.com/v1/public/yql?q=select%20LastTradePriceOnly%20from%20yahoo.finance.quote%20where%20symbol%20in%20(%221565.TWO%22%2C%222727.TW%22)&format=json&env=store%3A//datatables.org/alltableswithkeys&callback=', timeout = 3)
        self.assertEqual(d.result, expected_stocks)

    def test_query_async_failed(self):
        FakeResponse.status_code = 500
        FakeResponse.response = successful_response

        pq = PriceQuerier(treq)
        d = pq.query_async(['1565.TWO', '2727.TW'], 3)
        self.assertEqual(len(d.result), 0)

        FakeResponse.status_code = 200
        FakeResponse.response = error_response

        pq = PriceQuerier(treq)
        d = pq.query_async(['1565.TWO', '2727.TW'], 3)
        self.assertEqual(len(d.result), 0)


# class RealPriceQuerierTestCase(unittest.TestCase):
#     def test_query_async(self):
#         from twisted.internet import reactor
#
#         pq = PriceQuerier(treq)
#         r = pq.query_async(['1565.TWO', '2727.TW'], 3)
#         reactor.callLater(2, reactor.stop)
#         reactor.run()
#         for s in r.result:
#             print s
#
#     def test_query(self):
#         pq = PriceQuerier(requests)
#         stocks = pq.query(['1565.TWO', '2727.TW'], 3)
#         for s in stocks:
#             print s


class NameQuerierTestCase(unittest.TestCase):
    response = u'''<!doctype html>
                <html lang="zh-TW">
                <head>
                    <meta charset="utf-8">
                    <title>精華(1565)_即時行情_台股_WantGoo玩股網</title>
                </head>
                <body>
                </body>
                </html>'''
    def setUp(self):
        self.treq_get = treq.get
        treq.get = MagicMock(return_value = FakeResponse())

    def tearDown(self):
        treq.get = self.treq_get

    def test_query_async(self):
        FakeResponse.status_code = 200
        FakeResponse.response = NameQuerierTestCase.response

        querier = NameQuerier(treq)
        d = querier.query_async('1565.TWO', 3)
        self.assertEqual(d.result, u'精華')

    def test_query_async_failed(self):
        FakeResponse.status_code = 500
        FakeResponse.response = NameQuerierTestCase.response

        querier = NameQuerier(treq)
        d = querier.query_async('1565.TWO', 3)
        self.assertEqual(d.result.value.code, 500)
        d.addErrback(lambda _: None)


class NameQueryRetryTestCase(unittest.TestCase):
    def test_async_query_retry_no_retry(self):
        d = succeed(u'精華')
        attrs = {'query_async.return_value': d}
        querier = Mock(**attrs)
        retry = NameQueryRetry(querier)
        result = retry.query_async(u'1565.TWO', 3, 1, 10)

        self.assertEqual(result.result, u'精華')

    def test_async_query_retry_once(self):
        d1, d2 = fail(NameQueryException(500, 'some error')), succeed(u'精華')
        m1 = MagicMock(side_effect=[d1, d2])
        attrs = {'query_async': m1}
        querier = Mock(**attrs)
        retry = NameQueryRetry(querier)
        result = retry.query_async(u'1565.TWO', 3, 1, 10)

        def asserts(r):
            self.assertEqual(r, u'精華')
            self.assertEqual(querier.mock_calls, [call.query_async(u'1565.TWO', 3), call.query_async(u'1565.TWO', 3)])
        result.addCallback(asserts)

        return result



# class RealNameQuerierTestCase(unittest.TestCase):
#     def test_query_async(self):
#         from twisted.internet import reactor
#
#         pq = NameQuerier(treq)
#         r = pq.query_async('1565.TWO')
#         reactor.callLater(2, reactor.stop)
#         reactor.run()
#         print r.result
