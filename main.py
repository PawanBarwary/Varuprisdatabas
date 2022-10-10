import tkinter as tk
from db_handler import DbHandler, Request


class App:

    """ Main class for Graphical User Interface """

    root = tk.Tk()
    # Sets up window title
    root.title("Pawans Minikiosk 🌭")
    # Adds padding to window
    frame = tk.Frame(root, padx=30, pady=30)
    db_handler = DbHandler()
    products = [
        # Stores product objects from db
        product for product in db_handler.products if product.product_count > 0
    ]
    products_in_basket = {
        # Will store 'Row'-objects for products added to basket
    }

    def __init__(self):
        """ Sets up base layout """

        # Product input
        product_label = tk.Label(self.frame, text="Vara:")
        product_label.grid(row=1, column=0)
        # List of product names to be used in drop down menu
        product_options = [product.product_name for product in self.products]
        self.frame.grid()
        self.selected_product_variable = tk.StringVar(self.frame)
        # Sets default option in drop down menu
        self.selected_product_variable.set(product_options[0])
        product_drop_down = tk.OptionMenu(
            self.frame,
            self.selected_product_variable,
            *product_options,
            command=lambda x: self.change_product()
        )
        product_drop_down.grid(row=1, column=1)

        # Number Input
        number_label = tk.Label(self.frame, text="Antal:")
        number_label.grid(row=2, column=0)
        self.number_drop_down = NOItemsDropDown(
            self,
            self.db_handler,
            # Checks db for the number of products that can be offered
            self.db_handler.state[self.selected_product]
        )

        # Add to basket button
        select_button = tk.Button(
            self.frame,
            text="Lägg till i varukorgen",
            command=lambda: self.add_to_basket(
                self.selected_product,
                self.number_drop_down.selected_number
            )
        )
        select_button.grid(column=1)

    def change_product(self):
        """
        Is called when a user chooses a product in drop down.
        Changes the number of options you can choose to add to basket
        based on the new selected product
        """
        self.number_drop_down.update_no_options(
            self.db_handler.state[
                self.selected_product
            ]
        )

    def add_to_basket(self, product_name, number_of_items):
        """
        Function runs when you press 'Lägg till i varukorgen'
        Checks if product has already been added, in which case,
        that row is changed instead. Otherwise, a new one is created
        """
        if number_of_items == 0:
            return
        if product_name in self.products_in_basket.keys():
            row = self.products_in_basket[product_name]
            row.drop_down.set_selected_number(
                row.drop_down.selected_number + number_of_items
            )
            row.update_price_label()
            self.db_handler.add_request(Request(product_name, number_of_items))
            self.number_drop_down.update_no_options(
                self.db_handler.state[product_name]
            )
        else:
            if Row.row_number == 5:
                # If it is the first row of added products,
                # the submit button is also created
                SubmitButton(self)
            row = Row(
                self,
                self.db_handler,
                product_name,
                self.db_handler.get_no_in_db(
                    product_name
                ),
                self.db_handler.get_product_price(
                    product_name
                ),
                number_of_items
            )
            self.products_in_basket[product_name] = row
            # Modifies state of 'db_handler'
            self.db_handler.add_request(Request(product_name, number_of_items))
            # Lowers number of available items based on added items
            self.number_drop_down.update_no_options(
                self.db_handler.state[product_name]
            )

    @property
    def selected_product(self):
        """ Gets the string value from tkinter string variable object """
        return self.selected_product_variable.get()


class SubmitButton:

    """
    Class for submit button. When clicked, the user buys their added items
    """

    def __init__(self, app):
        """ Creates/styles button """
        self.app = app
        self.frame = app.frame
        button = tk.Button(
            self.frame,
            text="Köp varorna nedan: ",
            command=self.on_click
        )
        button.grid(row=4, column=1, pady=20)

    def on_click(self):
        """ Pushes changes to db on button event """
        self.app.db_handler.push_to_table()
        self.close_app()

    def close_app(self):
        """ Closes main window, and creates a 'thank-you' window """
        self.app.root.destroy()
        message_window = tk.Tk()
        message_window.geometry("300x100")
        message_window.title("Vi kommer att sakna dig😭😭😭")
        message = tk.Message(
            message_window, text="Tack för ditt köp. Välkommen åter!",
            width=300
        )
        message.grid()


class Row:

    " Class for row in basket "
    row_number = 5  # Class variable used for positioning of row in GUI

    def __init__(self, app, db, product_name, number_of_items, price, selected_number):
        """ Creates row """
        Row.row_number += 1
        self.app = app
        self.frame = app.frame
        self.product_name = product_name
        self.number_of_items = number_of_items
        self.price = price
        self.selected_number = selected_number

        product_label = tk.Label(self.frame, text=self.product_name)
        product_label.grid(row=self.row_number, column=0)
        self.drop_down = NOItemsDropDown(
            self.app, db, number_of_items, col=1, row_number=self.row_number, product=product_name, row=self
        )
        price_label = tk.Label(self.frame, text=f"{self.price}kr/st")
        price_label.grid(row=self.row_number, column=2, padx=40)
        total_price_label = tk.Label(
            self.frame, text=f"Totalt {self.price*self.selected_number}kr")
        total_price_label.grid(row=self.row_number, column=3)
        self.drop_down.set_selected_number(
            selected_number)  # Sets drop down value

    def update_price_label(self):
        """
        If the user changes the number of items in basket,
        the total price label will reflect that
        """
        total_price_label = tk.Label(
            self.frame,
            text=f"Totalt {round(self.price*self.drop_down.selected_number, 2)}kr"
        )
        total_price_label.grid(row=self.row_number, column=3)


class NOItemsDropDown:

    """ Class for numbered drop down menus """

    def __init__(self, app, db, number_of_items, col=1, row_number=2, row=None, product=None):
        self.app = app
        self.frame = app.frame
        self.db_handler = db
        self.number = number_of_items
        self.selected_number_variable = tk.IntVar()
        self.selected_number_variable.set(1)
        self.row = row
        self.product = product
        number_options = range(
            1, number_of_items + 1
        )

        self.number_drop_down = tk.OptionMenu(
            self.frame,
            self.selected_number_variable,
            *number_options,
            command=self.drop_down_command
        )
        self.number_drop_down.grid(row=row_number, column=col)

    def drop_down_command(self, number):
        """ Updates price label IF it is not the drop down in the form """
        self.update_basket(number)
        if self.row is not None:
            self.row.update_price_label()

    def update_basket(self, number_of_items):
        """ 
        If number of products is changed in checkout, the state is reset
        before a new request is added
        """
        if self.product:
            self.db_handler.reset_product_state(self.product)
            self.db_handler.add_request(Request(self.product, number_of_items))
            self.app.number_drop_down.update_no_options(
                self.db_handler.state[self.product]
            )

    def update_no_options(self, number_of_items):
        "Changes what numbers you can choose from in drop down"
        if number_of_items == 0:
            self.number_options = [0]
            self.set_selected_number(0)
        else:
            self.number_options = range(
                1, number_of_items + 1
            )
            self.set_selected_number(1)
        self.number_drop_down = tk.OptionMenu(
            self.frame,
            self.selected_number_variable,
            *self.number_options
        )

        print(f"{number_of_items=}")
        self.number_drop_down.grid(row=2, column=1)

    def set_selected_number(self, number):
        " Sets the number that is displayed as selected in drop down "
        self.selected_number_variable.set(number)

    @property
    def selected_number(self):
        " Gets value of selected_number variable as an integer "
        return self.selected_number_variable.get()


if __name__ == '__main__':
    app = App()
    app.frame.mainloop()
