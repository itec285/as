#!/bin/sh

# This file is typically called from the first-boot.py file

echo "First Boot" >> /home/pi/bootlog.txt

#Move Desktop wallpaper in.  This is a bit of a hack right now, as we are just moving ours to the default name.
cp /home/pi/as/road.jpg /usr/share/rpd-wallpaper/

#Change the splash screen to ours
cp /home/pi/as/splash.png /etc/splash.png
cp /home/pi/as/asplashscreen /etc/init.d/asplashscreen
chmod a+x /etc/init.d/asplashscreen
insserv /etc/init.d/asplashscreen
