from model.configuration import WatchConfigParser
from view.page import List


class ListStockController(object):
    def __init__(self, path):
        self.config_parser = WatchConfigParser()
        self.config_parser.parse(path)

    def list(self):
        conditions = self.config_parser.watch_conditions
        return List.format(conditions)
