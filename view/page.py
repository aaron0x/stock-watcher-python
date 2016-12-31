# -*- coding: utf-8 -*-

import HTML


class List(object):
    @staticmethod
    def format(content):
        title = ['代號', '買入價', '賣出價']
        stock_rows = []
        for c in content:
            stock_rows.append([c.number, c.low_price, c.high_price])

        return HTML.table([title] + stock_rows)
