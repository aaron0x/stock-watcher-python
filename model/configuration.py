import re


class WatchConditionParser(object):
    def __init__(self):
        self.watch_conditions = []

    def parse(self, config_obj):
        sections = config_obj.sections()
        stock_pattern = re.compile('^[0-9]{4}.(TWO|TW)$')
        for s in sections:
            if not re.search(stock_pattern, s):
                continue
            num = s
            low = config_obj.getfloat(s, 'low')
            high = config_obj.getfloat(s, 'high')
            self.watch_conditions.append(WatchCondition(num, low, high))


class LogConfigParser(object):
    def __init__(self):
        self.log_config = None

    def parse(self, config_obj):
        level = config_obj.get('Log', 'level')
        log_path = config_obj.get('Log', 'path')
        max_size = config_obj.getint('Log', 'max_size')
        backup_num = config_obj.getint('Log', 'backup_num')
        self.log_config = LogConfig(level, log_path, max_size, backup_num)


class WatchConfigParser(object):
    def __init__(self):
        self.to_addrs = []
        self.watch_conditions = []
        self.smtp_config = None
        self.query_timeout = 0
        self.log_config = None

    def parse(self, config_obj):
        self.to_addrs = config_obj.get('Notification', 'address').split(',')

        smtp_config_parser = SMTPConfigParser()
        smtp_config_parser.parse(config_obj)
        self.smtp_config = smtp_config_parser.smtp_config

        self.query_timeout = config_obj.getfloat('Query', 'timeout')

        log_config_parser = LogConfigParser()
        log_config_parser.parse(config_obj)
        self.log_config = log_config_parser.log_config

        watch_condition_parser = WatchConditionParser()
        watch_condition_parser.parse(config_obj)
        self.watch_conditions = watch_condition_parser.watch_conditions


class WebConfigParser(object):
    def __init__(self):
        self.watch_conditions = []
        self.smtp_config = None
        self.query_timeout = 0
        self.log_config = None
        self.db_path = None
        self.port = None

    def parse(self, config_obj):
        self.query_timeout = config_obj.getfloat('Query', 'timeout')

        log_config_parser = LogConfigParser()
        log_config_parser.parse(config_obj)
        self.log_config = log_config_parser.log_config

        watch_condition_parser = WatchConditionParser()
        watch_condition_parser.parse(config_obj)
        self.watch_conditions = watch_condition_parser.watch_conditions

        db_config_parser = RepositoryConfigParser()
        db_config_parser.parse(config_obj)
        self.db_path = db_config_parser.path

        self.port = config_obj.get('Web', 'port')


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


class SMTPConfig(object):
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


class SMTPConfigParser(object):
    def __init__(self):
        self.smtp_config = None

    def parse(self, config_obj):
        server = config_obj.get('SMTP', 'server')
        user = config_obj.get('SMTP', 'user')
        password = config_obj.get('SMTP', 'password')
        from_addr = config_obj.get('SMTP', 'from')
        subject = config_obj.get('SMTP', 'subject')
        self.smtp_config = SMTPConfig(server, user, password, from_addr, subject)


class LogConfig(object):
    def __init__(self, level, path, max_size, backup_num):
        self.level = level
        self.path = path
        self.max_size = max_size
        self.backup_num = backup_num

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False


class RepositoryConfigParser(object):
    def __init__(self):
        self.path = None

    def parse(self, config_obj):
        self.path = config_obj.get('Repository', 'path')


__all__ = ['WatchConfigParser', 'WebConfigParser']
