import logging
from logging.handlers import RotatingFileHandler


_logger = None


def init_logger(name, log_config):
    global _logger

    _logger = logging.getLogger(name)
    _logger.setLevel(log_config.level)
    handler = RotatingFileHandler(log_config.path, maxBytes=log_config.max_size,
                                  backupCount=log_config.backup_num)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    _logger.addHandler(handler)


def get_logger():
    global _logger
    return _logger

__all__ = ['get_logger', 'init_logger']
