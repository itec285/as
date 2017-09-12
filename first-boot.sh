#!/bin/sh

# This file is typically called from the first-boot.py file

echo "First Boot" >> /home/pi/bootlog.txt

#Move Desktop wallpaper in.  This is a bit of a hack right now, as we are just moving ours to the default name.
cp /home/pi/as/road.jpg /usr/share/rpd-wallpaper/

##Change the splash screen to ours - Old way with big screen, no longer used.
#cp /home/pi/as/splash-big.png /etc/splash-big.png
#cp /home/pi/as/asplashscreen /etc/init.d/asplashscreen
#chmod a+x /etc/init.d/asplashscreen
#insserv /etc/init.d/asplashscreen

#New way of changing the (smaller) splash screen at bootup
cp /home/pi/as/splash.png /usr/share/plymouth/themes/pix/splash.png

#Add the setup script to the home directory
cp /home/pi/as/setup.py /home/pi/setup.py

#Create a symbolic link from /usr/bin/setup to /home/pi/setup.py.  This will make it so users can type just 'setup' later.
ln -s /home/pi/setup.py /usr/bin/setup
