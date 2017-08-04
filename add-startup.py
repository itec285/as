searchstring = "@/home/pi/Till2.sh"
with open("/home/pi/.config/lxsession/LXDE-pi/autostart", "r+") as file:
    for line in file:
        if searchstring in line:
           break
    else: # not found, we are at the eof
        file.write(searchstring + '\n') # append missing data
