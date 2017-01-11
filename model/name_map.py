from twisted.internet.defer import inlineCallbacks
from twisted.internet.defer import returnValue
from twisted.internet.defer import DeferredList


class NameMapper(object):
    def __init__(self, name_repository, name_querier):
        self.name_repository = name_repository
        self.name_querier = name_querier

    @inlineCallbacks
    def map_async(self, numbers, timeout):
        def fill_name(name, i, num):
            names[i] = name
            self.name_repository.save_name(num, name)

        names = [None] * len(numbers)
        deferreds = []
        for i, s in enumerate(numbers):
            name = self.name_repository.get_name(s)
            if name:
                names[i] = name
            else:
                d = self.name_querier.query_async(s, timeout)
                d.addCallback(fill_name, i, s)
                deferreds.append(d)
        if deferreds:
            yield DeferredList(deferreds)
        returnValue(names)
