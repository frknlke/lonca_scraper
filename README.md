# lonca_scraper

A simplified scraper. Lonca_scraper extracts predetermined faetures from an XML file with the help of `ElementTree` mdoule.
During extraction operation, scraper directly uses `find()` method by giving desired "key" value. It also checks the availability of information to handle null pointer errors. For all features except "colors" it sets the value of unavailable information as empty string or None by default. For color fields, it sets the extracted information as array wihch consist of a single element that is an empty string. Since scraper creates a unqiue `stock_code` for each product as the concatenation of `productID` and `colors`, the process variation we apply for color fields allow us to prevent any undesirable behaviors during `stock_code` creation.

For product description field, scraper checks whether predefined word pattern exist in a product definiton in the XML file. In other words, it assumes that an information can exist in XML file with same "key" all the time. For example, during extraction of fabric information scraper checks whether `<strong>Kumaş Bilgisi:</strong>` pattern exists in the corresponding product definiton. If it exists, then start index of that information found as `start_index = description.find('<strong>Kumaş Bilgisi:</strong>') + len('<strong>Kumaş Bilgisi:</strong>')` . If an information does not exist in the product description, then its value is set as empty string. Similar workflows are used to extract other fields such as `product_measurements`, `model_measurements` etc.

After extraction completed, scraper creates a `product_detail` object to store information extracted from `ProductDetails` field of a product. Then it creates a `product` object to store all the information including `product_details`, `images`, `product_name`, description related information, and unique `stock_code`. In this step, objects are created to increase readability of the code since referencing a piece of information is much more straightforward in this case.

In final step, entries in the `MongoDB` are queried a filter that containes `stock_code` of current product as criteria. If there is an entry with the same `stock_code`, scraper performs not insertion but update operation to avoid duplicate entries. Otherwise, it performs regular insertion with all of the fields referenced from product object. During update, all fields excluding `createdAt` are updated with parameters we gave. 

To run the code:
Since lonca_scraper uses MongoDB to store entries, please install MongoDB by following the [installation guide](https://www.mongodb.com/docs/manual/installation/). After installing MongoDB successfully, pull the repository into your locale then locate where lonca_scraper folder is downloaded into. Since scraper uses external libraries, please install them first by entering following commands to your command line:

`pip install pymongo` \
`pip install unicode_tr`

After locating to directory that `main.py` exist, enter following into your command line.

`python main.py`

Then program starts execution. For each product entry in the XML file, it prompts whether that product exists in the database and whether or not update/insert operation completed successfully.








