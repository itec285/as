import os
from lxml import etree as ET

storeCode = raw_input('Enter the store code: ')
#print (storeCode)


#Write the results to an XML file

root = ET.Element("root")
doc = ET.SubElement(root, "doc")

ET.SubElement(doc, "field1", name="storeCode").text = storeCode
ET.SubElement(doc, "field2", name="asdfasd").text = "some vlaue2"

tree = ET.ElementTree(root)
tree.write("filename.xml", pretty_print=True)
