from pymongo import MongoClient
import xml.etree.ElementTree as ET
import product_details
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


def extract_fabric_info(description):
    if description.find('<strong>Kumaş Bilgisi:</strong>') == -1:
        print("Fabric info not found")
        return ""

    else:
        start_index = description.find('<strong>Kumaş Bilgisi:</strong>') + len('<strong>Kumaş Bilgisi:</strong>')
        end_index = description.find('</li>', start_index)
        fabric_info = description[start_index:end_index]
        print(fabric_info.strip())
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
        print(sample_size.strip().upper())
        return sample_size.strip().upper()


def extract_model_measurement(description):
    if description.find('<strong>Model Ölçüleri:</strong>') == -1:
        print("Model measurement info not found")
        return ""

    else:
        start_index = description.find('<strong>Model Ölçüleri:</strong>') + len('<strong>Model Ölçüleri:</strong>')
        end_index = description.find('</li>', start_index)
        model_measurement = description[start_index:end_index]

        print(model_measurement.strip())
        return model_measurement.strip()


def extract_product_measurement(description):
    if description.find('<strong>Ürün Ölçüleri') == -1:
        print("Product measurement info not found")
        return ""

    else:
        start_index = description.find('<strong>Ürün Ölçüleri') + len('<strong>Ürün Ölçüleri')
        start_index = description.find('</strong>', start_index) + len('</strong>')
        end_index = description.find('</li>', start_index)
        product_measurement = description[start_index:end_index]
        print(product_measurement.strip())
        return product_measurement.strip()


def product_description_parser(description):
    description = description.replace('&nbsp;', '')
    fabric_info = extract_fabric_info(description)
    extract_sample_size(description)
    extract_model_measurement(description)
    extract_product_measurement(description)
    pass


if __name__ == "__main__":
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
            if product_details is not None:
                product_details = [detail.attrib for detail in product_details.findall('ProductDetail')]

            else:
                product_details = []

            for detail in product_details:
                pass
                # print(detail)

            product_description = product.find('Description')
            if product_description is not None:
                product_description = product_description.text
                # print(product_description)
            else:
                product_description = ""

            product_description_parser(product_description)

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
