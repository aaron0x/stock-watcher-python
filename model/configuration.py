import codecs
import re
from ConfigParser import ConfigParser


class WatchConditionParser(object):
    def __init__(self):
        self.watch_conditions = []

    def parse(self, path):
        config_parser = ConfigParser()
        with codecs.open(path, 'r', 'UTF-8') as f:
            config_parser.readfp(f)
            sections = config_parser.sections()
            stock_pattern = re.compile('^[0-9]{4}.(TWO|TW)$')
            for s in sections:
                if not re.search(stock_pattern, s):
                    continue
                num = s
                low = config_parser.getfloat(s, 'low')
                high = config_parser.getfloat(s, 'high')
                self.watch_conditions.append(WatchCondition(num, low, high))


class LogSettingParser(object):
    def __init__(self):
        self.log_setting = None

    def parse(self, path):
        config_parser = ConfigParser()
        with codecs.open(path, 'r', 'UTF-8') as f:
            config_parser.readfp(f)

            level = config_parser.get('Log', 'level')
            log_path = config_parser.get('Log', 'path')
            max_size = config_parser.getint('Log', 'max_size')
            backup_num = config_parser.getint('Log', 'backup_num')
            self.log_setting = LogSetting(level, log_path, max_size, backup_num)


class WatchConfigParser(object):
    def __init__(self):
        self.to_addrs = []
        self.watch_conditions = []
        self.smtp_setting = None
        self.query_timeout = 0
        self.log_setting = None

    def parse(self, path):
        config_parser = ConfigParser()
        with codecs.open(path, 'r', 'UTF-8') as f:
            config_parser.readfp(f)

            self.to_addrs = config_parser.get('Notification', 'address').split(',')

            server = config_parser.get('SMTP', 'server')
            user = config_parser.get('SMTP', 'user')
            password = config_parser.get('SMTP', 'password')
            from_addr = config_parser.get('SMTP', 'from')
            subject = config_parser.get('SMTP', 'subject')
            self.smtp_setting = SMTPSetting(server, user, password, from_addr, subject)

            self.query_timeout = config_parser.getfloat('Query', 'timeout')

            log_setting_parser = LogSettingParser()
            log_setting_parser.parse(path)
            self.log_setting = log_setting_parser.log_setting

            watch_condition_parser = WatchConditionParser()
            watch_condition_parser.parse(path)
            self.watch_conditions = watch_condition_parser.watch_conditions


class WebConfig(object):
    def __init__(self):
        self.watch_conditions = []
        self.smtp_setting = None
        self.query_timeout = 0
        self.log_setting = None
        self.db_path = None

    def read(self, path):
        config_parser = ConfigParser()
        with codecs.open(path, 'r', 'UTF-8') as f:
            config_parser.readfp(f)

            self.query_timeout = config_parser.getfloat('Query', 'timeout')

            log_setting_parser = LogSettingParser()
            log_setting_parser.parse(path)
            self.log_setting = log_setting_parser.log_setting

            watch_condition_parser = WatchConditionParser()
            watch_condition_parser.parse(path)
            self.watch_conditions = watch_condition_parser.watch_conditions

            db_config_parser = DBConfigParser()
            db_config_parser.parse(path)
            self.db_path = db_config_parser.path


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


class LogSetting(object):
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


class DBConfigParser(object):
    def __init__(self):
        self.path = None

    def parse(self, path):
        config_parser = ConfigParser()
        with codecs.open(path, 'r', 'UTF-8') as f:
            config_parser.readfp(f)

            self.path = config_parser.get('DB', 'path')
