#!/usr/bin/env python
import os, subprocess

#Define a function to change part of a file
def inplace_change(filename, old_string, new_string):
    # Safely read the input filename using 'with'
    with open(filename) as f:
        s = f.read()
        if old_string not in s:
            print '"{old_string}" not found in {filename}.'.format(**locals())
            return

    # Safely write the changed content, if found in the file
    with open(filename, 'w') as f:
        print 'Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals())
        s = s.replace(old_string, new_string)
        f.write(s)

#Use the inplace change function to replace British (GB) keymapping with US Keyboard
inplace_change('/etc/default/keyboard','gb','us')

#Call the first boot shell script
subprocess.call(['home/pi/as/first-boot.sh'])
