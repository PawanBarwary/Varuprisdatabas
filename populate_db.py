import os
from os import path
from sqlalchemy.orm import sessionmaker
# Removes database file, if there
if os.path.exists(os.path.abspath("sqlalchemy.sqlite").replace("~", "")):
    os.remove("sqlalchemy.sqlite")
    print("Removing file")
else:
    print("File not there")
import table
print("Creating file")

# Products that will be added to the db, (name, number of items, price/item)
PRODUCTS = (
    ("Chips", 20, 15.5),
    ("Pepsi", 30, 10),
    ("Godis", 2, 35),
    ("Köttfärs", 3, 105.6),
    ("Billy's Panpizza", 20, 11),
    ("Kyckling", 29, 200),
    ("Shampoo", 36, 33),
    ("Dennis' Korv", 23, 12)
)


def populate_table():
    """
    Loops through 'PRODUCTS' and adds rows in table for each
    """
    Session = sessionmaker(bind=table.engine)
    session = Session()

    for i, item in enumerate(PRODUCTS):
        product_name, product_count, price = item
        new_row = table.Products(i, product_name, product_count, price)
        session.add(new_row)

    session.commit()
    print("Created and populated database")


populate_table()
