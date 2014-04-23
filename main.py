#!/usr/bin/env python3.3

import socket
import sys

xstart = 0
xstop  = 600
xstep  = 1
ystart = 0
ystop  = 600
ystep  = 1


host = sys.argv[1]
port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host,port))

def text(x, y, t):
	return 'TEXT {} {} {}\n'.format(x, y, t).encode('UTF-8')

def pixl(x, y, r, g, b):
	return 'PX {} {} {:02X}{:02X}{:02X}\n'.format(x, y, r, g, b).encode('UTF-8')

def makecon(text):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
	s.sendall(text)
	s.close()

def send(text):
	sock.sendall(text)

while True:
	for x in range(xstart, xstop, xstep):
		for y in range(ystart, ystop, ystep):
			send(pixl(x, y, x%255, y%255, 255-(x-y)%255))
