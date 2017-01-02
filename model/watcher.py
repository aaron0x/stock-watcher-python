from model.querier import Stock


class Watcher(object):
    def __init__(self, watch_config_parser, price_querier, notifier):
        self.watch_config_parser = watch_config_parser
        self.price_querier = price_querier
        self.notifier = notifier

    def watch(self):
        watched_conditions = self.watch_config_parser.watch_conditions
        if not watched_conditions:
            return
        watched_numbers = [c.number for c in watched_conditions]

        stocks = self.price_querier.query(watched_numbers, self.watch_config_parser.query_timeout)
        if not stocks:
            return

        conditional_stocks = [_ConditionalStock(ws[0], ws[1]) for ws in zip(watched_conditions, stocks)]
        out_of_range_conditional_stocks = [c for c in conditional_stocks if c.out_of_range()]
        if not out_of_range_conditional_stocks:
            return

        message = Watcher._to_message(out_of_range_conditional_stocks)
        self.notifier.notify(self.watch_config_parser.smtp_setting, self.watch_config_parser.to_addrs, message)

    @staticmethod
    def _to_message(out_of_range_conditional_stocks):
        message = []
        for cs in out_of_range_conditional_stocks:
            s = '{} is [{}], out of ({}, {})'.format(cs.number, cs.current_price, cs.low_price, cs.high_price)
            message.append(s)
        return '\n'.join(message)


class _ConditionalStock(Stock):
    def __init__(self, condition, stock):
        super(_ConditionalStock, self).__init__(stock.number, stock.current_price)
        self.condition = condition

    def out_of_range(self):
        return not (self.low_price < self.current_price < self.high_price)

    @property
    def low_price(self):
        return self.condition.low_price

    @property
    def high_price(self):
        return self.condition.high_price
