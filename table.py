from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float


engine = create_engine('sqlite:///sqlalchemy.sqlite', echo=True)
base = declarative_base()


class Products(base):
    """
    Class for SQLite Table that stores a code (id), product name
    product_count (how many there are) and the price per product
    """
    __tablename__ = "Products"
    code = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_count = Column(Integer)
    price = Column(Float)

    def __init__(self, code, product_name, product_count, price):
        self.code = code
        self.product_name = product_name
        self.product_count = product_count
        self.price = price


# Creates table in database
base.metadata.create_all(engine)
