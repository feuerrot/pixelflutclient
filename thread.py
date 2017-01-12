#!/usr/bin/env python3
import random
import socket
import sys
import threading
import time
from PIL import Image

xstart = 0
xstop  = 192
xstep  = 1
ystart = 0
ystop  = 32
ystep  = 1

host = sys.argv[1]
port = int(sys.argv[2])
image = str(sys.argv[3])

threads = []
commands = []

class pixelsender(threading.Thread):
	def __init__(self, host, port):
		super(pixelsender, self).__init__()
	
	def addpixel(self):
		self.cmd = commands[:]

	def run(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.addpixel()
		sock.connect((host,port))
		random.shuffle(self.cmd)
		subcmd = []
		while True:
			for elem in self.cmd:
				subcmd.append(elem)
				if len(subcmd) > 128:
					sock.sendall(b"".join(subcmd))
					subcmd = []

img = Image.open(image)
(a, b, ix, iy) = img.getbbox()

random.seed()

def rnd(a):
	return random.randint(0,a)

def command_pixel(x, y, r, g, b):
	return 'PX {} {} {:02X}{:02X}{:02X}\n'.format(x, y, r, g, b).encode('UTF-8')

# send reuses a connection - higher speed for pixel
def getsize(s):
	s.sendall('SIZE\n'.encode('UTF-8'))
	msg = s.recv(64).decode('UTF-8')
	(foo, xsize, ysize) = msg.split()
	print('Size: {}x{} px'.format(xsize,ysize))
	return (int(xsize), int(ysize))

# Get the size of the image
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((host,port))
	(xstop, ystop) = getsize(s)

def addpixel():
	print('Img:  {}x{} px'.format(ix, iy))
	print('addpixel')
	xstart = 0#xstop - ix
	ystart = 0#ystop - iy
	for x in range(xstop):
		for y in range(ystop):
			(r, g, b) = img.getpixel((x%ix,y%iy))
			commands.append(command_pixel(x+xstart, y+ystart, r, g, b))
	print('addedpixels')

try:
	addpixel()
	threads.append(pixelsender(host, port))
	threads.append(pixelsender(host, port))
	threads.append(pixelsender(host, port))
	threads.append(pixelsender(host, port))

	for elem in threads:
		elem.daemon = True
		elem.start()
	while True:
		time.sleep(1)

except KeyboardInterrupt:
	print('Beende Programm')
	exit(0)
except:
	print("Unexpected error:", sys.exc_info()[0])
	exit(1)
