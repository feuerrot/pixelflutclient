#!/usr/bin/env python3.3
import random
import socket
import sys

xstart = 0
xstop  = 800
xstep  = 1
ystart = 0
ystop  = 600
ystep  = 1

host = sys.argv[1]
port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host,port))

random.seed()

def rnd(a):
	return random.randint(0,a)

def command_text(x, y, t):
	return 'TEXT {} {} {}\n'.format(x, y, t).encode('UTF-8')

def command_pixel(x, y, r, g, b):
	return 'PX {} {} {:02X}{:02X}{:02X}\n'.format(x, y, r, g, b).encode('UTF-8')

# makecon makes a new connection for every text - higher speed for text
def makecon(command):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
	s.sendall(command)
	s.close()

# send reuses a connection - higher speed for pixel
def send(command):
	sock.sendall(command)

def text(x, y, t):
	makecon(command_text(x, y, t))

def pixl(x, y, r, g, b):
	send(command_pixel(x, y, r, g, b))

def getsize(s):
	s.sendall('SIZE\n'.encode('UTF-8'))
	msg = s.recv(64).decode('UTF-8')
	(foo, xsize, ysize) = msg.split()
	print('Size: {}x{} px'.format(xsize,ysize))
	return (int(xsize), int(ysize))


# define various draw functions here
def noise():
	pixl(rnd(xstop), rnd(ystop), rnd(255), rnd(255), rnd(255))
def blackrnd():
	pixl(rnd(xstop), rnd(ystop), 0, 0, 0)
def blacklin():
	for y in range(ystart, ystop, ystep):
		for x in range(xstart, xstop, xstep):
			pixl(x, y, 0, 0, 0)
# define various draw functions above


# Get the size of the image
(xstop, ystop) = getsize(sock)

######################
# Set the drawfunction
######################
draw = blacklin

try:
	while True:
		draw()
except KeyboardInterrupt:
	print('Beende Programm')
	exit(0)
except:
	print("Unexpected error:", sys.exc_info()[0])
	exit(1)
