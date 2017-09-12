#!/usr/bin/env python
import subprocess

#Make sure that the till session is in the auto start.  This will only add it if not already there.
searchstring = "@/home/pi/as/Till2.sh"
with open("/home/pi/.config/lxsession/LXDE-pi/autostart", "r+") as file:
    for line in file:
        if searchstring in line:
           break
    else: # not found, we are at the eof
        file.write(searchstring + '\n') # append missing data
        
##Call the script that will copy the wallpaper
#subprocess.call(['./first-boot.sh'])
