import json


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

    def query(self, stock_numbers):
        url = self._compose_url(stock_numbers)
        response =  self.request.get(url)
        return self._handle_response(response, stock_numbers)

    def _compose_url(self, stock_numbers):
        quoted_stock_numbers = [ '"{0}"'.format(n) for n in stock_numbers ]
        number_str = '({0})'.format(','.join(quoted_stock_numbers))
        url = 'https://query.yahooapis.com/v1/public/yql?q=select LastTradePriceOnly from yahoo.finance.quote where symbol in {0}&format=json&env=store://datatables.org/alltableswithkeys&callback='.format(number_str)
        return url

    def _handle_response(self, response, stock_numbers):
        if response.status_code != 200:
            return []
        response_json = json.loads(response.text)
        if response_json['query']['count'] != len(stock_numbers):
            return []
        quote = response_json['query']['results']['quote']
        stocks = []
        for i, q in enumerate(quote):
            number = stock_numbers[i]
            price = float(q['LastTradePriceOnly'])
            stocks.append(Stock(number, price))
        return stocks
