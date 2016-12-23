import urllib

from twisted.internet.defer import inlineCallbacks, returnValue


class Stock(object):
    def __init__(self, number, current_price):
        self.number = number
        self.current_price = current_price

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False


class PriceQuerier(object):
    def __init__(self, request):
        self.request = request

    @inlineCallbacks
    def query_async(self, stock_numbers):
        url = self._compose_url(stock_numbers)
        r = yield self.request.get(url)
        if r.code != 200:
            returnValue([])
        response = yield r.json()
        returnValue(self._handle_response(response, stock_numbers))

    def _compose_url(self, stock_numbers):
        quoted_stock_numbers = ['"{}"'.format(n) for n in stock_numbers]
        number_str = '({})'.format(','.join(quoted_stock_numbers))
        select_str = 'select LastTradePriceOnly from yahoo.finance.quote where symbol in {}&format=json&env=store://datatables.org/alltableswithkeys&callback='.format(number_str)
        escaped_str = urllib.quote(select_str, '/()&=')
        url = 'https://query.yahooapis.com/v1/public/yql?q={}'.format(escaped_str)
        return url

    def _handle_response(self, response, stock_numbers):
        if response['query']['count'] != len(stock_numbers):
            return []
        quote = response['query']['results']['quote']
        stocks = []
        for i, q in enumerate(quote):
            number = stock_numbers[i]
            price = float(q['LastTradePriceOnly'])
            stocks.append(Stock(number, price))
        return stocks
