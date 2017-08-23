#!/bin/sh

# This file is typically called from the first-boot.py file

echo "First Boot" >> /home/pi/bootlog.txt
cp /home/pi/as/road.jpg /usr/share/rpd-wallpaper/
