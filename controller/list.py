from twisted.internet.defer import inlineCallbacks
from twisted.internet.defer import returnValue
from klein import Klein

from model.configuration import WatchCondition
from view.page import List


class ListStockController(object):
    app = Klein()

    def __init__(self, config, stock_name_mapper):
        self.config = config
        self.stock_name_mapper = stock_name_mapper
        self.named_watch_conditions = None

    @app.route('/stocks')
    @inlineCallbacks
    def list_async(self, _):
        if self.named_watch_conditions is None:
            conditions = self.config.watch_conditions
            stock_nums = [c.number for c in conditions]
            stock_names = yield self.stock_name_mapper.map_async(stock_nums, self.config.query_timeout)
            self.named_watch_conditions = [NamedWatchCondition(i[0], i[1]) for i in zip(stock_names, conditions)]

        returnValue(List.format(self.named_watch_conditions))


class NamedWatchCondition(WatchCondition):
    def __init__(self, name, condition):
        super(NamedWatchCondition, self).__init__(condition.number, condition.low_price, condition.high_price, condition.skip_notif)
        self.name = name
