import os, subprocess

#For getting our IP address - requests is external, everything else is internal
import socket, fcntl, struct, requests

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

internalIPAddress = get_ip_address('eth0')  # should return something like '192.168.0.110'
#print ('The internal IP address is: ' + internalIPAddress)

externalIPAddress = requests.get('https://ipapi.co/ip/').text
#print ('The external IP address is: ' + externalIPAddress)

#Ask the important questions, and then create the XML File
from lxml import etree as ET

storeCode = raw_input('Enter the store code: ')
#print (storeCode)

tillNumber = raw_input('Enter the till number: ')
#print (tillNumber)

#Write the results to an XML file
root = ET.Element("root")
doc = ET.SubElement(root, "doc")

ET.SubElement(doc, "field1", name="storeCode").text = storeCode
ET.SubElement(doc, "field2", name="tillNumber").text = tillNumber
ET.SubElement(doc, "field3", name="internalIPAddress").text = internalIPAddress
ET.SubElement(doc, "field4", name="externalIPAddress").text = externalIPAddress

tree = ET.ElementTree(root)
tree.write("filename.xml", pretty_print=True)

#Prepare the system to run till2
print ('SAY YES')
subprocess.call(['./Till2.sh'])
