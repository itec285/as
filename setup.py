#!/usr/bin/env python

import os, subprocess, json, urllib

#For getting our IP address - requests is external, everything else is internal
import socket, fcntl, struct, requests

#Define the base address of the RDP information / registration web service
#serviceurl = 'http://localhost:5000/starplus/api/v1.0/rdplogin/'
serviceurl = 'http://159.203.41.250:5000/starplus/api/v1.0/rdplogin/'

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def get_RDP_data(storeCode, authCode, tillNumber):
	url = serviceurl + storeCode + '/' + authCode + '/' + tillNumber
	#print ('Retrieving',url)
	uh = urllib.urlopen(url)
	data = uh.read()
	#print ('Retrieved',len(data),'characters')
	try: js = json.loads(str(data))
	except: js = None
	RDPData= js['data']
	
	#Below lines are for debugging only.
	#print (json.dumps(js, indent=4))
	#print ('--------------')
	#print (js['data'])
	#print type(RDPData)
	#print len(RDPData)
	#print ('RDP Address is:',RDPData[0]['RDPAddress'])
	#print ('RDP Port is:',RDPData[0]['RDPPort'])
	#print ('RDP Login is:',RDPData[0]['RDPLogin'])
	#print ('RDP Password is:',RDPData[0]['RDPPassword'])
	
	return (RDPData)

internalIPAddress = get_ip_address('eth0')  # should return something like '192.168.0.110'
#print ('The internal IP address is: ' + internalIPAddress)

externalIPAddress = requests.get('https://ipapi.co/ip/').text
#print ('The external IP address is: ' + externalIPAddress)

#Ask the important questions
storeCode = raw_input('Enter the store code: ')
#print (storeCode)

authCode = raw_input('Enter your authorization number: ')
#print (tillNumber)

tillNumber = raw_input('Enter the till number: ')
#print (tillNumber)

#Get a dictionary of our RDP server address, port, login, and password given our storecode, authorization number (secret), and tillNumber
RDPData = get_RDP_data(storeCode, authCode, tillNumber)

#Below lines are for debugging only.
#print ('RDP Address is:',RDPData[0]['RDPAddress'])
#print ('RDP Port is:',RDPData[0]['RDPPort'])
#print ('RDP Login is:',RDPData[0]['RDPLogin'])
#print ('RDP Password is:',RDPData[0]['RDPPassword'])

RDPAddress = RDPData[0]['RDPAddress']
RDPPort = str(RDPData[0]['RDPPort'])
RDPLogin = RDPData[0]['RDPLogin']
RDPPassword = RDPData[0]['RDPPassword']

#Write the results to an XML file
#Import the needed module
from lxml import etree as ET

root = ET.Element("root")
doc = ET.SubElement(root, "doc")

ET.SubElement(doc, "field1", name="storeCode").text = storeCode
ET.SubElement(doc, "field1", name="authCode").text = authCode
ET.SubElement(doc, "field3", name="tillNumber").text = tillNumber
ET.SubElement(doc, "field4", name="internalIPAddress").text = internalIPAddress
ET.SubElement(doc, "field5", name="externalIPAddress").text = externalIPAddress
ET.SubElement(doc, "field6", name="RDPAddress").text = RDPAddress
ET.SubElement(doc, "field7", name="RDPPort").text = RDPPort
ET.SubElement(doc, "field8", name="RDPLogin").text = RDPLogin
ET.SubElement(doc, "field9", name="RDPPassword").text = RDPPassword

tree = ET.ElementTree(root)
tree.write("configuration.xml", pretty_print=True)

#Prepare the system to run till2
print ('SAY YES')
subprocess.call(['./Till2.sh'])
