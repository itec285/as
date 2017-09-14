#!/usr/bin/env python
import os, subprocess

loginFile='/home/pi/login.sh'

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

def create_login_file(path):
	f = open(path,"w")
	f.write('#!/bin/sh' + '\n')
	f.write('lxterminal --command=setup' + '\n')
	f.close()

def make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2    # copy R bits to X
    os.chmod(path, mode)
        
#Use the inplace change function to replace British (GB) keymapping with US Keyboard
inplace_change('/etc/default/keyboard','gb','us')

create_login_file(loginFile)
make_executable(loginFile)

#Call the first boot shell script
subprocess.call(['/home/pi/as/first-boot.sh'])
