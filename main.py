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
	return 'px {} {} {:02X}{:02X}{:02X}\n'.format(x, y, r, g, b).encode('UTF-8')

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
	send(command_pixel(x, y, r, g, b))
	#print(command_pixel(x, y, r, g, b))

def getsize(s):
	s.sendall('SIZE\n'.encode('UTF-8'))
	msg = s.recv(64).decode('UTF-8')
	(foo, xsize, ysize) = msg.split()
	print('Size: {}x{} px'.format(xsize,ysize))
	return (int(xsize), int(ysize))


# define various draw functions here
def block(x, y, dx, dy, r, g, b):
	for xa in range(dx):
		for ya in range(dy):
			pixl(x+xa, y+ya, r, g, b)

def colorbow():
	for x in range(xstart, xstop, xstep):
		for y in range(ystart, ystop, ystep):
			#pixl(x, y, 30,30,30)
			pixl(x, y, int((4*y-x)%255), int((x+y)%255), int((3*x-y*5)%255)) #int(((math.cos((3*y+2*x)%2*math.pi)+1)/2)*255), int(((math.sin((y+2*x)%2*math.pi)+1)/2)*255))

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
def blockrnd():
	block(rnd(xstop), rnd(ystop), rnd(50), rnd(50), rnd(255), rnd(255), rnd(255))

def textspam():
	text(rnd(xstop), rnd(ystop), 'Könnt Ihr das mal in c neuschreiben?')

# define various draw functions above


# Get the size of the image
(xstop, ystop) = getsize(sock)

######################
# Set the drawfunction
######################
draw = textspam

try:
	while True:
		draw()
		time.sleep(0.1)
except KeyboardInterrupt:
	print('Beende Programm')
	exit(0)
except:
	print("Unexpected error:", sys.exc_info()[0])
	exit(1)
