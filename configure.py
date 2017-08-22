import os, subprocess

#For getting our IP address
import socket, fcntl, struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

internal_IPAddress = get_ip_address('eth0')  # should return something like '192.168.0.110'

#Ask the important questions, and then create the XML File
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

#Prepare the system to run till2
print ('SAY YES')
subprocess.call(['./Till2.sh'])
