import logging
from logging.handlers import RotatingFileHandler


logger = None


def init_logger(name, log_config):
    global logger

    logger = logging.getLogger(name)
    logger.setLevel(log_config.level)
    handler = RotatingFileHandler(log_config.path, maxBytes=log_config.max_size,
                                  backupCount=log_config.backup_num)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def get_logger():
    global logger
    return logger
