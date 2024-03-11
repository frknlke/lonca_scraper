from pymongo import MongoClient
import xml.etree.ElementTree as ET
import product_details_class
import product

"""
client = MongoClient('localhost', 27017)

print(client.list_database_names())

tree = ET.parse('lonca-sample.xml')
root = tree.getroot()

print(root.__len__())
print(root[0].__len__())

print(root[0][0])
print(root[0][0][0].attrib)

for image in root[0][0]:
    print(image.attrib)

"""
"""def tokenize_string(string):
    return string.split()"""


def make_camel_case(string):
    string = string.lower()
    return string.title()


def create_placeholder_product_details():
    # Create a placeholder product details object if ProductDetails is not found in the XML.
    # Assign None to all fields except colors, which is a list only consists of an empty string.
    # This is done to prevent any possible errors that may occur during the object creation.
    # Since colors are used in stock code generation, it is important to have a placeholder for it.
    return product_details_class.ProductDetails(None, "USD", None, False, None, None, [""], None, None, None)


def extract_and_objectize_product_details(product_details):
    price_unit = "USD"
    product_type = make_camel_case(product_details.find("./ProductDetail[@Name='ProductType']").get('Value')) if product_details.find(
        "./ProductDetail[@Name='ProductType']") is not None else None

    quantity = int(product_details.find("./ProductDetail[@Name='Quantity']").get('Value')) if product_details.find(
        "./ProductDetail[@Name='Quantity']") is not None else None

    price_element = product_details.find("./ProductDetail[@Name='Price']").get('Value') if product_details.find(
        "./ProductDetail[@Name='Price']") is not None else None
    price = float(price_element.replace(',', '.')) if price_element is not None else None

    discounted_price_element = product_details.find("./ProductDetail[@Name='DiscountedPrice']").get('Value') \
        if product_details.find(
        "./ProductDetail[@Name='DiscountedPrice']") is not None else None
    discounted_price = float(discounted_price_element.replace(',', '.')) if discounted_price_element is not None else None

    is_discounted = price > discounted_price if price is not None and discounted_price is not None else False

    series = make_camel_case(product_details.find("./ProductDetail[@Name='Series']").get('Value')).upper() if product_details.find(
        "./ProductDetail[@Name='Series']") is not None else None

    # set colors to a list of camel cased color names if there is any, otherwise set it to a list that contains an empty string only
    colors_element = [make_camel_case(product_detail.attrib['Value']) for product_detail in product_details.findall(
        "./ProductDetail[@Name='Color']")] if len(product_details.findall('./ProductDetail[@Name="Color"]')) != 0 else [""]

    season_element = product_details.find("./ProductDetail[@Name='Season']").get('Value') if product_details.find(
        "./ProductDetail[@Name='Season']") is not None else ""

    season = season_element.split()[1] if season_element != "" else ""
    year = season_element.split()[0] if season_element != "" else ""

    product_details_instance = product_details_class.ProductDetails(
        price, price_unit, discounted_price, is_discounted, product_type,
        quantity, colors_element, series, season, year)

    #print(product_details_instance)
    return product_details_instance


def extract_fabric_info(description):
    if description.find('<strong>Kumaş Bilgisi:</strong>') == -1:
        #print("Fabric info not found")
        return ""

    else:
        start_index = description.find('<strong>Kumaş Bilgisi:</strong>') + len('<strong>Kumaş Bilgisi:</strong>')
        end_index = description.find('</li>', start_index)
        fabric_info = description[start_index:end_index]
        #print(fabric_info.strip())
        return fabric_info.strip()


def extract_sample_size(description):
    if description.find('<li>Modelin üzerindeki ürün <strong>') == -1:
        print("Sample size info not found")
        return ""

    else:
        start_index = description.find('<li>Modelin üzerindeki ürün <strong>') + len(
            '<li>Modelin üzerindeki ürün <strong>')
        end_index = description.find('</strong>', start_index)
        sample_size = description[start_index:end_index]
        #print(sample_size.strip().upper())
        return sample_size.strip().upper()


def extract_model_measurement(description):
    if description.find('<strong>Model Ölçüleri:</strong>') == -1:
        #print("Model measurement info not found")
        return ""

    else:
        start_index = description.find('<strong>Model Ölçüleri:</strong>') + len('<strong>Model Ölçüleri:</strong>')
        end_index = description.find('</li>', start_index)
        model_measurement = description[start_index:end_index]
        #print(model_measurement.strip())
        return model_measurement.strip()


def extract_product_measurement(description):
    if description.find('<strong>Ürün Ölçüleri') == -1:
        #print("Product measurement info not found")
        return ""

    else:
        start_index = description.find('<strong>Ürün Ölçüleri') + len('<strong>Ürün Ölçüleri')
        start_index = description.find('</strong>', start_index) + len('</strong>')
        end_index = description.find('</li>', start_index)
        product_measurement = description[start_index:end_index]
        #print(product_measurement.strip())
        return product_measurement.strip()


def product_description_parser(description):
    description = description.replace('&nbsp;', '')
    fabric_info = extract_fabric_info(description)
    extract_sample_size(description)
    extract_model_measurement(description)
    extract_product_measurement(description)
    pass


if __name__ == "__main__":
    #print(make_camel_case("hELLO, world!"))
    client = MongoClient('localhost', 27017)
    print(client.list_database_names())
    db_instance = client.lonca

    # To discriminate whether the operation is an update on existing data or a new data insertion from scratch
    is_update = True
    products = None
    if "products" not in db_instance.list_collection_names():
        is_update = False
        products = db_instance.create_collection("products")

    else:
        products = db_instance.products

    # will be changed later
    is_update = False
    if is_update:
        pass

    else:
        tree = ET.parse('lonca-sample.xml')
        root = tree.getroot()

        for product in root.findall('Product'):
            images_element = product.find('Images')
            if images_element is not None:
                product_images = [str(image.attrib.get('Path')) for image in images_element.findall('Image')]
            else:
                product_images = []

            product_details = product.find('ProductDetails')
            product_details_object = extract_and_objectize_product_details(product_details) if product_details is not None else create_placeholder_product_details()
            """            if product_details is not None:
                #product_details = [detail for detail in product_details.findall('ProductDetail')]
                extract_and_objectize_product_details(product_details)

            else:
                product_details = []
"""
            print(product_details_object)
            product_description = product.find('Description')
            if product_description is not None:
                product_description = product_description.text
                # print(product_description)
            else:
                product_description = ""

            product_description_parser(product_description)
            print("-------------------")

    """
    tree = ET.parse('lonca-sample.xml')
    root = tree.getroot()

    print(root.__len__())
    print(root[0].__len__())

    print(root[0][0])
    print(root[0][0][0].attrib)

    for image in root[0][0]:
        print(image.attrib)

    """
