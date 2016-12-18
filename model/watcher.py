class Watcher(object):
    def __init__(self, watch_config_parser, price_querier, notifier):
        self.watch_config_parser = watch_config_parser
        self.price_querier = price_querier
        self.notifier = notifier

    def watch(self, config_path):
        self.watch_config_parser.read(config_path)
        watched_conditions = self.watch_config_parser.watch_conditions
        watched_numbers = [c.number for c in watched_conditions]
        stocks = self.price_querier.query(watched_numbers)
        conditionalStocks = [_ConditionalStock(ws[0], ws[1]) for ws in zip(watched_conditions, stocks)]
        out_of_range_conditionalStocks = [c for c in conditionalStocks if c.out_of_range()]
        message = self._to_message(out_of_range_conditionalStocks)
        self.notifier.notify(self.watch_config_parser, message)

    def _is_out_of_price(self, condition_stock):
        condition = condition_stock[0]
        stock = condition_stock[1]
        return not (condition.low_price < stock.current_price < condition.high_price)

    def _to_message(self, out_of_range_conditionalStocks):
        message = []
        for cs in out_of_range_conditionalStocks:
            s = '{0} is [{1}], out of ({2}, {3})'.format(cs.number, cs.current_price, cs.low_price, cs.high_price)
            message.append(s)
        return '\n'.join(message)


class _ConditionalStock(object):
    def __init__(self, condition, stock):
        self.condition = condition
        self.stock = stock

    def out_of_range(self):
        return not (self.low_price < self.current_price < self.high_price)

    @property
    def number(self):
        return self.stock.number

    @property
    def current_price(self):
        return self.stock.current_price

    @property
    def low_price(self):
        return self.condition.low_price

    @property
    def high_price(self):
        return self.condition.high_price


