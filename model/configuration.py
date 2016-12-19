from ConfigParser import ConfigParser


class WatchConfigParser(object):
    def __init__(self):
        self.to_addrs = []
        self.watch_conditions = []
        self.smtp_setting = None

    def read(self, path):
        config_parser = ConfigParser()
        config_parser.read(path)

        self.to_addrs = config_parser.get('Notification', 'address').split(',')
        config_parser.remove_section('Notification')

        server = config_parser.get('SMTP', 'server')
        user = config_parser.get('SMTP', 'user')
        password = config_parser.get('SMTP', 'password')
        from_addr = config_parser.get('SMTP', 'from')
        subject = config_parser.get('SMTP', 'subject')
        self.smtp_setting = SMTPSetting(server, user, password, from_addr, subject)
        config_parser.remove_section('SMTP')

        sections = config_parser.sections()
        for s in sections:
            num = s
            low = config_parser.getfloat(s, 'low')
            high = config_parser.getfloat(s, 'high')
            self.watch_conditions.append(WatchCondition(num, low, high))


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

class SMTPSetting(object):
    def __init__(self, server, user, password, from_addr, subject):
        self.server = server
        self.user = user
        self.password = password
        self.from_addr = from_addr
        self.subject = subject

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
