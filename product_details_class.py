# Author: Furkan Ülke
# This file is created to define the product details class and its attributes.
# product_details_class.py

class ProductDetails:
    def __init__(self, price, price_unit, discounted_price, is_discounted, product_type, quantity, colors, series, season, year):
        self.price = price
        self.price_unit = price_unit
        self.discounted_price = discounted_price
        self.is_discounted = is_discounted
        self.product_type = product_type
        self.quantity = quantity
        self.colors = colors
        self.series = series
        self.season = season
        self.year = year

    def __str__(self):
        return (f"Price: {self.price} {self.price_unit}\n"
                f"Discounted Price: {self.discounted_price} {self.price_unit}\n"
                f"Is Discounted: {self.is_discounted}\n"
                f"Product Type: {self.product_type}\n"
                f"Quantity: {self.quantity}\n"
                f"Colors: {self.colors}\n"
                f"Series: {self.series}\n"
                f"Season: {self.season}\n"
                f"Year: {self.year}")


