import urllib

from retrying import retry
from twisted.internet.defer import inlineCallbacks, returnValue, Deferred


class Stock(object):
    def __init__(self, number, current_price):
        self.number = number
        self.current_price = current_price

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __str__(self):
        return '({},{})'.format(self.number, self.current_price)


class PriceQuerier(object):
    def __init__(self, request):
        self.request = request

    @retry(stop_max_attempt_number=3, wait_fixed=3000)
    def query(self, stock_numbers, timeout):
        url = self._compose_url(stock_numbers)
        response = self.request.get(url, timeout=timeout)
        if response.status_code != 200:
            return []
        return PriceQuerier._handle_response(stock_numbers, response.json())

    @inlineCallbacks
    def query_async(self, stock_numbers, timeout):
        url = PriceQuerier._compose_url(stock_numbers)
        r = yield self.request.get(url, timeout=timeout)
        if r.code != 200:
            returnValue([])
        response = yield r.json()
        returnValue(self._handle_response(stock_numbers, response))

    @staticmethod
    def _compose_url(stock_numbers):
        quoted_stock_numbers = ['"{}"'.format(n) for n in stock_numbers]
        number_str = '({})'.format(','.join(quoted_stock_numbers))
        select_str = 'select LastTradePriceOnly from yahoo.finance.quote where symbol in {}&format=json&env=store://datatables.org/alltableswithkeys&callback='.format(number_str)
        escaped_str = urllib.quote(select_str, '/()&=')
        url = 'https://query.yahooapis.com/v1/public/yql?q={}'.format(escaped_str)
        return url

    @staticmethod
    def _handle_response(stock_numbers, response):
        if response['query']['count'] != len(stock_numbers):
            return []
        quote = response['query']['results']['quote']
        stocks = []
        for i, q in enumerate(quote):
            number = stock_numbers[i]
            price = float(q['LastTradePriceOnly'])
            stocks.append(Stock(number, price))
        return stocks


class NameQuerier(object):
    def __init__(self, request):
        self.request = request

    @inlineCallbacks
    def query_async(self, number, timeout):
        url = 'http://www.wantgoo.com/stock/' + number[:4] + '?searchType=stocks'
        r = yield self.request.get(url, timeout=timeout)
        response = yield r.text()
        if r.code != 200:
            raise NameQueryException(r.code, response)
        returnValue(self.parse_response_body(response))

    @staticmethod
    def parse_response_body(response):
        name_start = response.find("<title>") + len("<title>")
        name_end = response.find("(", name_start)
        return response[name_start:name_end]


class RetriedNameQuerier(object):
    def __init__(self, querier):
        self.querier = querier

    @inlineCallbacks
    def query_async(self, number, timeout, retry_num=2, retry_interval_ms=1000):
        while True:
            try:
                d = yield self.querier.query_async(number, timeout)
                returnValue(d)
            except NameQueryException:
                from twisted.internet import reactor

                if retry_num > 0:
                    def f():
                        d.callback(None)
                    retry_num -= 1
                    dc = reactor.callLater(retry_interval_ms / 1000, f)
                    d = Deferred(dc.cancel)
                    yield d
                else:
                    raise


class NameQueryException(Exception):
    def __init__(self, code, msg):
        super(NameQueryException, self).__init__(msg)
        self.code = code
