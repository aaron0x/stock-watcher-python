import sys
import codecs
import traceback
from ConfigParser import ConfigParser

import treq

from model.logger import get_logger
from model.configuration import WebConfigParser
from model.repository import StockNameRepository
from model.stock_name_map import StockNameMapper
from model.querier import NameQuerier
from controller.list import ListStockController

def main():
    if len(sys.argv) != 2:
        sys.stderr.write('useage: program <config_path>\n')
        return

    try:
        config_path = sys.argv[1]
        with codecs.open(config_path, 'r', 'utf-8') as f:
            config = ConfigParser()
            config.readfp(f)
            parser = WebConfigParser()
            parser.parse(config)
        logger = get_logger('web', parser.log_config)
    except:
        sys.stderr.write('parse config error:' +  traceback.format_exc())
        return

    try:
        repository = StockNameRepository(parser.db_path)
        querier = NameQuerier(treq)
        stock_name_mapper = StockNameMapper(repository, querier)
        controller = ListStockController(parser, stock_name_mapper)
        controller.app.run('0.0.0.0', 8080)
    except:
        logger.error(traceback.format_exc())

if __name__ == '__main__':
    main()
