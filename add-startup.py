#!/usr/bin/env python
import subprocess, os

configFile='/home/pi/configuration.xml'

#Make sure that the till session is in the auto start.  This will only add it if not already there.
searchstring = "@/home/pi/login.sh"
with open("/home/pi/.config/lxsession/LXDE-pi/autostart", "r+") as file:
    for line in file:
        if searchstring in line:
           break
    else: # not found, we are at the eof
        file.write(searchstring + '\n') # append missing data
