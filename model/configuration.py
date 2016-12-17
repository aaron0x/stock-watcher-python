from ConfigParser import ConfigParser


class WatchConfigParser(object):
    def read(self, path):
        config_parser = ConfigParser()
        config_parser.read(path)
        sections = config_parser.sections()
        conditions = []
        for s in sections:
            num = s
            low = config_parser.getfloat(s, "low")
            high = config_parser.getfloat(s, "high")
            conditions.append(WatchCondition(num, low, high))
        return conditions


class WatchCondition(object):
    def __init__(self, number, low_price, high_price):
        self.number = number
        self.low_price = low_price
        self.high_price = high_price

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False