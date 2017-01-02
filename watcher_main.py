import sys
import traceback

import requests
import smtplib

from model.configuration import WatchConfigParser
from model.querier import PriceQuerier
from model.notification import Notifier
from model.watcher import Watcher
from model.logger import get_logger


def main():
    if len(sys.argv) != 2:
        sys.stderr.write('useage: program <config_path>\n')
        return
    config_path = sys.argv[1]

    try:
        watch_config_parser = WatchConfigParser()
        watch_config_parser.parse(config_path)
        logger = get_logger('Watcher', watch_config_parser.log_setting)
    except:
        sys.stderr.write(traceback.format_exc())
        return

    logger.info('Start!')
    try:
        price_querier = PriceQuerier(requests)
        notifier = Notifier(smtplib.SMTP_SSL)

        w = Watcher(watch_config_parser, price_querier, notifier)
        w.watch()
    except:
        logger.error(traceback.format_exc())
    logger.info('End!')


if __name__ == "__main__":
    main()
