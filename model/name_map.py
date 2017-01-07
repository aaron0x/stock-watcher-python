from twisted.internet.defer import inlineCallbacks
from twisted.internet.defer import returnValue

class NameMapper(object):
    def __init__(self, name_repository, name_querier):
        self.name_repository = name_repository
        self.name_querier = name_querier

    @inlineCallbacks
    def map_async(self, numbers, timeout):
        names = []
        for s in numbers:
            name = self.name_repository.get_name(s)
            if not name:
                name = yield self.name_querier.query_async(s, timeout)
                self.name_repository.save_name(s, name)
            names.append(name)
        returnValue(names)
