# -*- coding: utf-8 -*-

import HTML


class List(object):
    @staticmethod
    def format(stocks):
        # HTML.table doesn't support unicode, convert to utf-8 first.
        title = [u'代號'.encode('utf-8'), u'名稱'.encode('utf-8'), u'買入價'.encode('utf-8'), u'賣出價'.encode('utf-8')]
        stock_rows = []
        for s in stocks:
            stock_rows.append([s.number[:4].encode('utf-8'), s.name.encode('utf-8'), str(s.low_price), str(s.high_price)])

        return '<meta charset="UTF-8">' + HTML.table([title] + stock_rows)
