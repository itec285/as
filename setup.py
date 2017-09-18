#!/usr/bin/env python

import os, subprocess, json, urllib, sys

#For getting our IP address - requests is external, everything else is internal
import socket, fcntl, struct, requests

#Define the base address of the RDP information / registration web service
#serviceurl = 'http://localhost:5000/starplus/api/v1.0/rdplogin/'
#serviceurl = 'http://159.203.41.250:5000/starplus/api/v1.0/rdplogin/'
serviceurl = 'https://www.asregister.tk/starplus/api/v1.0/'

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def register(storeCode, tillNumber, externalIPAddress, internalIPAddress):
	url = serviceurl + 'register/' + storeCode + '/' + tillNumber + '/' + externalIPAddress + '/' + internalIPAddress
	print ('Retrieving',url)
	uh = urllib.urlopen(url)
	data = uh.read()
	try: js = json.loads(str(data))
	except: js = None
	
	#Debugging lines
	#print(js)
	#print(js['data'])
	
	try:
		RegisterData= js['data']
	except TypeError as e:
			#print ('Type error - No or invalid data returned from server:' + str(e))  #use for additional debugging
			print ('Type error - No or invalid data returned from server.')
			print('SETUP FAILED - COULD NOT REGISTER SYSTEM')
			raw_input("Press Enter to continue..")
			sys.exit(1)

def get_RDP_data(storeCode, authCode, tillNumber):
	url = serviceurl + 'rdplogin/' + storeCode + '/' + authCode + '/' + tillNumber
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

def create_login_file(RDPAddress, RDPPort, RDPLogin, RDPPassword):
	f = open("login.sh","w")
	f.write('#!/bin/sh' + '\n')
	f.write('while true' + '\n')
	f.write('do' + '\n')
	f.write('    ' + 'sleep 1' + '\n')
	f.write('    ' + 'if [ -f configuration.xml ]; then' + '\n')
	#In the xfreerdp line below, the /f forces fullscreen and will 'lock-down' the pi desktop from casual users (not experts).
	#  Also, note that the /cert-ignore is a temporary hack for demo purposes.  This should note be done in production.  Instead,
	#  get a real, signed certificate for the RDP Server (also note that this likely is in fact required for PCI)
	f.write('    ' + '    ' + 'xfreerdp /v:' + RDPAddress + ' /u:' + RDPLogin + ' /p:' + RDPPassword + ' /cert-ignore' + ' /f' + ' || echo "$(date) : Failed to login to RDP Server" >> errorlog.txt' +'\n')
	f.write('    ' + 'else' + '\n')
	f.write('    ' + '    ' + 'echo "$(date) : No configuration.xml file found.  Running setup." >> errorlog.txt' +'\n')
	f.write('    ' + '    ' + 'lxterminal --command setup' +'\n')
	f.write('    ' + 'fi' + '\n')
	f.write('done' + '\n')
	f.close()

def make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2    # copy R bits to X
    os.chmod(path, mode)

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

#Register this system.
try:
	register(storeCode, tillNumber, externalIPAddress, internalIPAddress)
except IOError as e:
	print ("I/O error({0}):{1}".format(e.errno, e.strerror))
	print('SETUP FAILED - COULD NOT OBTAIN RDP INFORMATION')
	raw_input("Press Enter to continue..")
	sys.exit(1)

#Get a dictionary of our RDP server address, port, login, and password given our storecode, authorization number (secret), and tillNumber
try:
	RDPData = get_RDP_data(storeCode, authCode, tillNumber)
except IOError as e:
	print ("I/O error({0}):{1}".format(e.errno, e.strerror))
	print('SETUP FAILED - COULD NOT OBTAIN RDP INFORMATION')
	raw_input("Press Enter to continue..")
	sys.exit(1)
except TypeError as e:
	print ("Type error - No or invalid data returned from server.")
	print('SETUP FAILED - COULD NOT OBTAIN RDP INFORMATION')
	raw_input("Press Enter to continue..")
	sys.exit(1)

#Below lines are for debugging only.
#print ('RDP Address is:',RDPData[0]['RDPAddress'])
#print ('RDP Port is:',RDPData[0]['RDPPort'])
#print ('RDP Login is:',RDPData[0]['RDPLogin'])
#print ('RDP Password is:',RDPData[0]['RDPPassword'])

try:
	RDPAddress = RDPData[0]['RDPAddress']
	RDPPort = str(RDPData[0]['RDPPort'])
	RDPLogin = RDPData[0]['RDPLogin']
	RDPPassword = RDPData[0]['RDPPassword']
except Exception, e:
	print ('SETUP FAILED - INVALID RDP INFORMATION RETURNED:' + str(e))
	RDPAddress = RDPPort = RDPLogin = RDPPassword = 'NOT AVAILABLE'
	sys.exit(1)

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

create_login_file(RDPAddress, RDPPort, RDPLogin, RDPPassword)
make_executable('login.sh')
print('\n\n\n\n')

print('SETUP COMPLETED SUCCESSFULLY')
raw_input("Press Enter to continue and reboot...")
subprocess.call(['sudo', 'init', '6'])
