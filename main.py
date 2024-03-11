# Author: Furkan Ülke

# Description: This script reads the products from the XML file and inserts or updates the products in the MongoDB database.
# The script uses the product and product_details classes to increase the readability and re-usability of the code.
# The script also uses the unicode_tr library to handle the Turkish characters in the product names.
# The script also uses the datetime library to get the current date and time to set the createdAt and updatedAt fields of the products.
# The script also uses the pymongo library to connect to the MongoDB database and perform the insertion and update operations.
# The script also uses the xml.etree.ElementTree library to parse the XML file.

# Import the required libraries
from datetime import datetime
from pymongo import MongoClient
import xml.etree.ElementTree as ET
from unicode_tr import unicode_tr

# Import the required classes
import product_details_class
import product_class


# Create a unique stock code for the product using the product number and the color.
def create_unique_stock_code(product_number, color):
    # The stock code is created by concatenating the product number and the colors.
    product_colors = [color.lower() for color in color]
    concatenated_colors = "-".join(product_colors)

    # If there is no color, the stock code is created using only the product number.
    stock_code_value = f"{product_number}-{concatenated_colors}" if product_colors[0] != '' else product_number
    return stock_code_value


# Convert the given string to camel case and return the camel cased string.
# I used unicode_tr to handle the Turkish characters in the product names. 'İ' is converted to 'i' and 'I' is converted to 'ı' etc.
def make_camel_case(string_value):
    string_value = unicode_tr(f"{string_value}")
    string_value = string_value.lower()
    return string_value.title()


def create_placeholder_product_details():
    # Create a placeholder product details object if ProductDetails is not found in the XML.
    # Assign None to all fields except colors, which is a list only consists of an empty string.
    # This is done to prevent any possible errors that may occur during the object creation.
    # Since colors are used in stock code generation, it is important to have a placeholder for it.
    return product_details_class.ProductDetails(None, "USD", None, False, None, None, [""], None, None, None)


# Extract product details from the XML and create a ProductDetails object using the extracted data.
# Then return the created ProductDetails object.
def extract_and_objectize_product_details(product_details):
    price_unit = "USD"

    # Extract product type, quantity, price, discounted price, series, colors, season, and year from the XML if they exist.
    # Then create a ProductDetails object using the extracted data.
    # If any of the fields do not exist in the XML, assign None to the corresponding field except colors, which is a list only consists of an empty string.
    product_type = make_camel_case(
        product_details.find("./ProductDetail[@Name='ProductType']").get('Value')) if product_details.find(
        "./ProductDetail[@Name='ProductType']") is not None else None

    quantity = int(product_details.find("./ProductDetail[@Name='Quantity']").get('Value')) if product_details.find(
        "./ProductDetail[@Name='Quantity']") is not None else None

    price_element = product_details.find("./ProductDetail[@Name='Price']").get('Value') if product_details.find(
        "./ProductDetail[@Name='Price']") is not None else None
    price = float(price_element.replace(',', '.')) if price_element is not None else None

    discounted_price_element = product_details.find("./ProductDetail[@Name='DiscountedPrice']").get('Value') \
        if product_details.find(
        "./ProductDetail[@Name='DiscountedPrice']") is not None else None
    discounted_price = float(
        discounted_price_element.replace(',', '.')) if discounted_price_element is not None else None

    # Check if the product is discounted by comparing the price and the discounted price
    is_discounted = price > discounted_price if price is not None and discounted_price is not None else False

    series = make_camel_case(
        product_details.find("./ProductDetail[@Name='Series']").get('Value')).upper() if product_details.find(
        "./ProductDetail[@Name='Series']") is not None else None

    # set colors to a list of camel cased color names if there is any, otherwise set it to a list that contains an empty string only
    colors_element = [make_camel_case(product_detail.attrib['Value']) for product_detail in product_details.findall(
        "./ProductDetail[@Name='Color']")] if len(product_details.findall('./ProductDetail[@Name="Color"]')) != 0 else [
        ""]

    season_element = product_details.find("./ProductDetail[@Name='Season']").get('Value') if product_details.find(
        "./ProductDetail[@Name='Season']") is not None else ""

    season = season_element.split()[1] if season_element != "" else ""
    year = season_element.split()[0] if season_element != "" else ""

    # Create a ProductDetails object using the extracted data
    product_details_instance = product_details_class.ProductDetails(
        price, price_unit, discounted_price, is_discounted, product_type,
        quantity, colors_element, series, season, year)

    return product_details_instance


# Extract fabric info from the product description.
# Then return the extracted fabric info as a string.
def extract_fabric_info(description):
    if description.find('<strong>Kumaş Bilgisi:</strong>') == -1:
        # If fabric info does not exist, return an empty string
        return ""

    else:
        # If fabric info exists, extract and return the fabric info
        # by finding the start and end indices of the fabric info in the description
        start_index = description.find('<strong>Kumaş Bilgisi:</strong>') + len('<strong>Kumaş Bilgisi:</strong>')
        end_index = description.find('</li>', start_index)
        fabric_info = description[start_index:end_index]
        return fabric_info.strip()


# Extract sample size from the product description.
# Then return the extracted sample size info as a uppercase string.
def extract_sample_size(description):
    if description.find('<li>Modelin üzerindeki ürün <strong>') == -1:
        # If sample size info does not exist, return an empty string
        return ""

    else:
        # If sample size info exists, extract and return the sample size info
        # by finding the start and end indices of the sample size info in the description
        start_index = description.find('<li>Modelin üzerindeki ürün <strong>') + len(
            '<li>Modelin üzerindeki ürün <strong>')
        end_index = description.find('</strong>', start_index)
        sample_size = description[start_index:end_index]
        return sample_size.strip().upper()


# Extract model measurements from the product description.
# Then return the extracted model measurement info as a string.
def extract_model_measurement(description):
    if description.find('<strong>Model Ölçüleri:</strong>') == -1:
        # If model measurement info does not exist, return an empty string
        return ""

    else:
        # If model measurement info exists, extract and return the model measurement info
        # by finding the start and end indices of the model measurement info in the description
        start_index = description.find('<strong>Model Ölçüleri:</strong>') + len('<strong>Model Ölçüleri:</strong>')
        end_index = description.find('</li>', start_index)
        model_measurement = description[start_index:end_index]
        return model_measurement.strip()


# Extract product measurements from the product description.
# Then return the extracted product measurement info as a string.
def extract_product_measurement(description):
    # Check if the product measurement info exists in the description
    if description.find('<strong>Ürün Ölçüleri') == -1:
        # If product measurement info does not exist, return an empty string
        return ""

    else:
        # if product measurement info exists, extract and return the product measurement info
        # by finding the start and end indices of the product measurement info in the description
        start_index = description.find('<strong>Ürün Ölçüleri') + len('<strong>Ürün Ölçüleri')
        start_index = description.find('</strong>', start_index) + len('</strong>')
        end_index = description.find('</li>', start_index)
        product_measurement = description[start_index:end_index]
        return product_measurement.strip()


# Trigger the corresponding functions to extract the fabric info, sample size,
# model measurements, and product measurements from the product description.
# Then return the extracted data as a tuple.
def product_description_parser(description):
    # Remove the non-breaking space character from the description
    description = description.replace('&nbsp;', '')
    fabric_info = extract_fabric_info(description)
    sample_size = extract_sample_size(description)
    model_measurements = extract_model_measurement(description)
    product_measurements = extract_product_measurement(description)
    return fabric_info, sample_size, model_measurements, product_measurements


if __name__ == "__main__":
    # Create a MongoDB client
    client = MongoClient('localhost', 27017)

    # Create a database for the project if it does not exist, otherwise use the existing database
    db_instance = client.lonca

    # Create a collection for the products if it does not exist, otherwise use the existing collection
    products_collection = db_instance.create_collection("products") if "products" not in db_instance.list_collection_names() else db_instance.products

    tree = ET.parse('big-sample.xml')
    root = tree.getroot()

    # Iterate through the products in the XML file
    for product in root.findall('Product'):
        # Extract product images from the XML if it exists, otherwise set it to an empty list
        product_images = [str(image.attrib.get('Path')) for image in product.find('Images').findall('Image')] \
            if product.find('Images') is not None else []

        # Extract product details from the XML if it exists, otherwise create a placeholder product details object
        product_details = product.find('ProductDetails')
        product_details_object = extract_and_objectize_product_details(product_details) \
            if product_details is not None else create_placeholder_product_details()

        # Extract product description from the XML if it exists, otherwise set it to an empty string
        product_description = product.find('Description').text if product.find('Description') is not None else ""

        # Extract fabric info, sample size, model measurements, and product measurements from the product description
        fabric_info, sample_size, model_measurements, product_measurements = product_description_parser(
            product_description)

        # Extract product_id and product_name from the XML from product attributes
        product_id, product_name = product.attrib['ProductId'], make_camel_case(product.attrib['Name'])

        # Create a unique stock code for the product using the product number and the color.
        stock_code = create_unique_stock_code(product_id, product_details_object.colors)

        # Create a Product object using the extracted data
        # I used the product and product_details classes to increase the readability and re-usability of the code.
        product_entry = product_class.Product(product_name, product_id, stock_code, product_details_object,
                                              product_images, fabric_info, sample_size, model_measurements,
                                              product_measurements)

        # Ternary operator to check if the product exists in the database
        entry_exists = True if products_collection.find_one({"stock_code": product_entry.stock_code}) else False

        # Create a dictionary to insert or update the product in the database
        db_product_entry = {
            "stock_code": product_entry.stock_code,
            "color": product_entry.product_details.colors,
            "discounted_price": product_entry.product_details.discounted_price,
            "images": product_entry.product_images,
            "is_discounted": product_entry.product_details.is_discounted,
            "name": product_entry.product_name,
            "price": product_entry.product_details.price,
            "price_unit": product_entry.product_details.price_unit,
            "product_type": product_entry.product_details.product_type,
            "quantity": product_entry.product_details.quantity,
            "sample_size": product_entry.sample_size,
            "series": product_entry.product_details.series,
            "status": "Active" if product_entry.product_details.quantity > 0 else "Inactive",
            "fabric": product_entry.fabric,
            "model_measurements": product_entry.model_measurements,
            "product_measurements": product_entry.product_measurements,
            "season": product_entry.product_details.season,
            "year": product_entry.product_details.year,
            "createdAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "updatedAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        }
        if entry_exists:
            # if the product already exists in the database, update all fields except the createdAt field
            filter_query = {"stock_code": product_entry.stock_code}

            if entry_exists:
                # do not update the createdAt field if the product already exists in the database
                del db_product_entry["createdAt"]

            # update the product if it exists in the database
            result = products_collection.update_one(filter_query, {"$set": db_product_entry})
            if result.modified_count:
                print(f"Product with stock code {product_entry.stock_code} updated successfully")
            else:
                print(f"Product with stock code {product_entry.stock_code} update operation failed")
        else:
            print(f"Product with stock code {product_entry.stock_code} does not exist in the database, so insert operation will be performed")
            # insert the product to the database if it does not exist
            result = products_collection.insert_one(db_product_entry)
            if result.inserted_id:
                print(f"Product inserted successfully with id: {result.inserted_id}")
            else:
                print("Product insertion failed")

    # Find a product with the given query. I used it to test the insertion and update operations.
    """query = {"name": "Nakışlı Elbise"}
    result = products_collection.find(query)
    if result:
        for product in result:
            print("Product found with the given query")
            print(product)
    else:
        print("No product found with the given query")
    """

    # Delete all products from the collection. I leaved this part commented out to prevent accidental deletion of the products.
    """result = products_collection.delete_many({})
    if result.deleted_count:
        print(f"{result.deleted_count} products deleted successfully")
    else:
        print("No product deleted")
    """
    client.close()
