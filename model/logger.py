import logging
from logging.handlers import RotatingFileHandler


def get_logger(name, log_setting):
    logger = logging.getLogger(name)
    logger.setLevel(log_setting.level)
    handler = RotatingFileHandler(log_setting.path, maxBytes=log_setting.max_size,
                                  backupCount=log_setting.backup_num)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
