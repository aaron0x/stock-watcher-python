from twisted.internet.defer import inlineCallbacks
from twisted.internet.defer import returnValue

class StockNameMapper(object):
    def __init__(self, name_repository, name_querier):
        self.name_repository = name_repository
        self.name_querier = name_querier

    @inlineCallbacks
    def map_async(self, stock_numbers):
        names = []
        for s in stock_numbers:
            name = self.name_repository.get_name(s)
            if not name:
                name = yield self.name_querier.query_async(s)
                self.name_repository.save_name(s, name)
            names.append(name)
        returnValue(names)
