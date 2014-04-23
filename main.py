#!/usr/bin/env python3.3

import socket
import sys


host = sys.argv[1]
port = int(sys.argv[2])

string = 'R3K'

def text(x, y, t):
	return 'TEXT {} {} {}\n'.format(x, y, t).encode('UTF-8')

def pixl(x, y, r, g, b):
	return 'PX {} {} {:02X}{:02X}{:02X}\n'.format(x, y, r, g, b).encode('UTF-8')

def makecon(text):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
	s.sendall(text)
	s.close()

while True:
	for x in range(100, 800):
		for y in range(100, 600):
			makecon(pixl(x, y, x%255, y%255, (x+y)%255))
