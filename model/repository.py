from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData
from sqlalchemy.schema import Table
from sqlalchemy.schema import Column
from sqlalchemy.types import String
from sqlalchemy.sql import select


class StockNameRepository(object):
    def __init__(self, path):
        self.engine = create_engine("sqlite:///" + path)

        metadata = MetaData()
        self.stocks = Table('stock', metadata,
                       Column('number', String(), primary_key=True),
                       Column('name', String(), nullable=False))
        metadata.create_all(self.engine)

    def get_name(self, number):
        s = select([self.stocks]).where(self.stocks.c.number == number)
        conn = self.engine.connect()
        result = conn.execute(s).fetchone()
        conn.close()
        if result:
            return result[1]
        else:
            return result

    def save_name(self, number, name):
        conn = self.engine.connect()
        i = self.stocks.insert().values(number=number, name=name)
        conn.execute(i)
        conn.close()
