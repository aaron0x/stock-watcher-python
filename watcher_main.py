import logging
import sys
import traceback
from logging.handlers import RotatingFileHandler

import requests
import smtplib

from model.configuration import WatchConfigParser
from model.querier import PriceQuerier
from model.notification import Notifier
from model.watcher import Watcher


def main():
    if len(sys.argv) != 2:
        sys.stderr.write('useage: program <config_path>\n')
        return
    config_path = sys.argv[1]

    try:
        watch_config_parser = WatchConfigParser()
        watch_config_parser.read(config_path)
        logger = get_logger(watch_config_parser.log_setting)
    except:
        sys.stderr.write(traceback.format_exc())
        return

    logger.info('Start!')
    try:
        price_querier = PriceQuerier(requests)
        notifier = Notifier(smtplib.SMTP_SSL())

        w = Watcher(watch_config_parser, price_querier, notifier)
        w.watch()
    except:
        logger.error(traceback.format_exc())
    logger.info('End!')


def get_logger(log_setting):
    logger = logging.getLogger("Stock Watcher")
    logger.setLevel(log_setting.level)
    handler = RotatingFileHandler(log_setting.path, maxBytes=log_setting.max_size,
                                  backupCount=log_setting.backup_num)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

if __name__ == "__main__":
    main()
