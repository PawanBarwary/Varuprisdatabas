from typing import List
import table
from sqlalchemy.orm import sessionmaker


class Request:
    """ Class for requests """

    def __init__(self, product_name, amount):
        self.product_name = product_name
        self.amount = amount


class DbHandler:

    """ Class for database interactions """
    products: List[table.Products] = []

    def __init__(self):
        Session = sessionmaker(bind=table.engine)
        self.session = Session()
        self.products = self.session.query(table.Products).all()
        self.state = {
            product.product_name: product.product_count for product in self.products
        }
        self.read()

    def read(self):
        """ Prints everything available in db"""
        for row in self.session.query(table.Products).all():
            print(row.code, row.product_name, row.product_count, row.price)

    def add_request(self, req: Request):
        """ Updates state """
        if req.amount <= self.state[req.product_name] and req.amount > 0:
            self.state[req.product_name] -= req.amount
            return True
        return False

    def reset_product_state(self, product_name):
        """
        Resets state of a given product.
        Meaning that everything in the db is available for selection again
        """
        db_product = next(
            filter(
                lambda x: x.product_name == product_name,
                self.products
            )
        )
        self.state[product_name] = db_product.product_count

    def get_no_in_db(self, product_name):
        """ Gets number of items available in db for a product """
        row = next(
            filter(
                lambda x: x.product_name ==
                product_name, self.products
            )
        )
        return row.product_count

    def get_product_price(self, product_name):
        """ Gets price per item for a product """
        row = next(
            filter(
                lambda x: x.product_name ==
                product_name, self.products
            )
        )
        return row.price

    def push_to_table(self):
        """ Pushes DbHandler 'state' to db """
        for product, count in self.state.items():
            row = next(
                filter(
                    lambda x: x.product_name == product, self.products
                )
            )
            row.product_count = count
        self.session.commit()
