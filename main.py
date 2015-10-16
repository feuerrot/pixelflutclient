#!/usr/bin/env python3
import random
import socket
import sys
import time
import math

xstart = 0
xstop  = 1024
xstep  = 1
ystart = 0
ystop  = 768
ystep  = 1

host = sys.argv[1]
port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host,port))

random.seed()

def rnd(a):
	return random.randint(0,a)

def command_text(x, y, t):
	return 'text {} {} {}\n'.format(x, y, t).encode('UTF-8')

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
	send(command_text(x, y, t))

def pixl(x, y, r, g, b):
	send(command_pixel(x, y, int(r%256), int(g%256), int(b%256)))
	#print(command_pixel(x, y, r, g, b))

def pixlbw(x, y, bw):
	send(command_pixel(x, y, int(bw%256), int(bw%256), int(bw%256)))

def getsize(s):
	s.sendall('SIZE\n'.encode('UTF-8'))
	msg = s.recv(64).decode('UTF-8')
	(foo, xsize, ysize) = msg.split()
	print('Size: {}x{} px'.format(xsize,ysize))
	return (int(xsize), int(ysize))


def colorize(x, y):
	#if (x % 3 == y % 3):
	#	pixlbw(x, y, 255)
	pixl(x, y, math.cos(math.sin(math.tan(x+y)))/(math.cos(math.tan(math.sin(y)))+1)*255, math.sin(math.cos(math.tan((x*y)%math.pi+11)))*math.sin(math.cos(math.tan(y%255))), (ystop-y+1)/(xstop-x+1)*255)

# define various draw functions here
def block(x, y, dx, dy, r, g, b):
	for xa in range(dx):
		for ya in range(dy):
			pixl(x+xa, y+ya, r, g, b)

def colorbow():
	for x in range(xstart, xstop, xstep):
		for y in range(ystart, ystop, ystep):
			colorize(x,y)
def noise():
	pixl(rnd(xstop), rnd(ystop), rnd(255), rnd(255), rnd(255))

def noiselin():
	for y in range(ystart, ystop, ystep):
		for x in range(xstart, xstop, xstep):
			pixl(x, y, rnd(255), rnd(255), rnd(255))
def whiternd():
	pixl(rnd(xstop), rnd(ystop), 0, 0, 0)

def whitelin():
	for y in range(ystart, ystop, ystep):
		for x in range(xstart, xstop, xstep):
			pixl(x, y, 255, 255, 255)
def blackrnd():
	pixl(rnd(xstop), rnd(ystop), 255, 255, 255)

def blacklin():
	for y in range(ystart, ystop, ystep):
		for x in range(xstart, xstop, xstep):
			pixl(x, y, 0, 0, 0)
		#locallist = pixellist[]#[:int(len(pixellist)/2)]
def blockrnd():
	block(rnd(xstop), rnd(ystop), rnd(10), rnd(10), rnd(255), rnd(255), rnd(255))

def textspam():
	text(rnd(xstop), rnd(ystop), 'Könnt Ihr das mal in c neuschreiben?')

# define various draw functions above


# Get the size of the image
(xstop, ystop) = getsize(sock)

######################
# Set the drawfunction
######################
draw = blockrnd

try:
	while True:
		draw()
except KeyboardInterrupt:
	print('Beende Programm')
	exit(0)
except:
	print("Unexpected error:", sys.exc_info()[0])
	exit(1)
