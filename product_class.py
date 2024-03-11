# Author: Furkan Ülke
# This file is created to define the product class and its attributes.
# product_class.py
import product_details_class

class Product:
    def __init__(self, product_name, product_id, stock_code, product_details, product_images, fabric, sample_size,
                 model_measurements, product_measurements):
        self.product_name = product_name
        self.product_id = product_id
        self.stock_code = stock_code
        self.product_details = product_details
        self.product_images = product_images
        self.fabric = fabric
        self.sample_size = sample_size
        self.model_measurements = model_measurements
        self.product_measurements = product_measurements

    def __str__(self):
        return (f"Product Name: {self.product_name}\n"
                f"Product ID: {self.product_id}\n"
                f"Stock Code: {self.stock_code}\n"
                f"Product Details: {self.product_details}\n"
                f"Product Images: {self.product_images}\n"
                f"Fabric: {self.fabric}\n"
                f"Sample Size: {self.sample_size}\n"
                f"Model Measurements: {self.model_measurements}\n"
                f"Product Measurements: {self.product_measurements}")
