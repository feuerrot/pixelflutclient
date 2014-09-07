#!/usr/bin/env python3
import random
import socket
import sys
import threading
import time
from PIL import Image

xstart = 0
xstop  = 1024
xstep  = 1
ystart = 0
ystop  = 768
ystep  = 1

host = sys.argv[1]
port = int(sys.argv[2])
image = str(sys.argv[3])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host,port))

img = Image.open(image)
(a, b, ix, iy) = img.getbbox()

pixellist = list()
random.seed()

ratio = 100

def rnd(a):
	return random.randint(0,a)

def command_pixel(x, y, r, g, b):
	return 'px {} {} {:02X}{:02X}{:02X}\n'.format(x, y, r, g, b).encode('UTF-8')

# send reuses a connection - higher speed for pixel
def send(command):
	sock.sendall(command)

def pixl(x, y, r, g, b):
	send(command_pixel(x, y, r, g, b))

def getsize(s):
	s.sendall('SIZE\n'.encode('UTF-8'))
	msg = s.recv(64).decode('UTF-8')
	(foo, xsize, ysize) = msg.split()
	print('Size: {}x{} px'.format(xsize,ysize))
	return (int(xsize), int(ysize))

# image draw functions only

# Get the size of the image
(xstop, ystop) = getsize(sock)

######################
# Set the drawfunction
######################



def addpixel():
	print('addpixel')
	xstart = xstop//2 - ix//2
	ystart = ystop//2 - iy//2
	for x in range(ix):
		for y in range(iy):
			(r, g, b) = img.getpixel((x,y))
			pixellist.append([x+xstart,y+ystart,r,g,b])
	print('addedpixels')

def printpixl():
	addpixel()
	while True:
		random.shuffle(pixellist)
		locallist = pixellist[:int(len(pixellist)/10)]
		for elem in locallist:
			(x, y, r, g, b) = locallist.pop()
			if (r != 255 and b != 255 and g != 255):
				pixl(x, y, r, g, b)


try:
	printpxl = threading.Thread(target=printpixl)
	printpxl.daemon = True
	printpxl.start()
	printpxl.join()

except KeyboardInterrupt:
	print('Beende Programm')
	exit(0)
#except:
#	print("Unexpected error:", sys.exc_info()[0])
#	exit(1)
