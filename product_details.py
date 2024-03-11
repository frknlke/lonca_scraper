
class ProductDetails:
    def __init__(self, price, discounted_price, product_type, quantity, color, series, season):
        self.price = price
        self.discounted_price = discounted_price
        self.product_type = product_type
        self.quantity = quantity        ## Must be integer
        self.color = color
        self.series = series
        self.season = season
        self.price_unit = "USD"
        # self.sample_size = sample_size handle it. Must be uppercase
        # self.fabric = fabric handle it.
        # self.is_discounted = self.price > self.discounted_price


