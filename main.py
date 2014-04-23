#!/usr/bin/env python3.3

import socket
import sys


host = sys.argv[1]
port = int(sys.argv[2])

string = 'R3K'



def makecon(text):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
	s.sendall(text)
	s.close()

while True:
	for x in range(0, 600, 60):
		for y in range(0, 600, 20):
			send = 'TEXT {} {} {}\n'.format(x, y, string).encode('UTF-8')
			makecon(send)
