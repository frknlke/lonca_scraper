# product.py
import product_details_class

class Product:
    def __init__(self, product_name, price, discounted_price, product_type, quantity, color, series, season):
        self.product_details = product_details.ProductDetails(price, discounted_price, product_type, quantity, color, series, season)
        # self.stock_code = None handle it according to the answer
        # self.name = product_name handle it. Must be uppercase

