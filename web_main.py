import sys

import treq

from model.configuration import WebConfig
from model.repository import StockNameRepository
from model.stock_name_map import StockNameMapper
from model.querier import NameQuerier
from controller.list import ListStockController

def main():
    if len(sys.argv) != 2:
        sys.stderr.write('useage: program <config_path>\n')
        return

    config_path = sys.argv[1]
    config = WebConfig()
    config.read(config_path)
    repository = StockNameRepository(config.db_path)
    querier = NameQuerier(treq)
    stock_name_mapper = StockNameMapper(repository, querier)
    controller = ListStockController(config, stock_name_mapper)
    controller.app.run('0.0.0.0', 8080)

if __name__ == '__main__':
    main()
