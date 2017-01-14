import traceback

from twisted.internet.defer import inlineCallbacks
from twisted.internet.defer import returnValue
from twisted.internet.defer import DeferredList

from logger import get_logger


class NameMapper(object):
    def __init__(self, name_repository, name_querier):
        self.name_repository = name_repository
        self.name_querier = name_querier

    @inlineCallbacks
    def map_async(self, numbers, timeout):
        def fill_name(result, index, num):
            names[index] = result
            self.name_repository.save_name(num, result)

        names = [''] * len(numbers)
        deferreds = []
        for i, s in enumerate(numbers):
            name = self.name_repository.get_name(s)
            if name:
                names[i] = name
            else:
                try:
                    d = self.name_querier.query_async(s, timeout)
                    d.addCallback(fill_name, i, s)
                    deferreds.append(d)
                except:
                    get_logger().error(traceback.format_exc())
        if deferreds:
            yield DeferredList(deferreds)
        returnValue(names)
