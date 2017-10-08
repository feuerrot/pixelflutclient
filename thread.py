#!/usr/bin/env python3
import random
import socket
import sys
import threading
import time
from PIL import Image

xstart = None
xstop  = 192
xstep  = 1
ystart = None
ystop  = 32
ystep  = 1

host = sys.argv[1]
port = int(sys.argv[2])
image = str(sys.argv[3])
try:
	xstart = int(sys.argv[4])
	ystart = int(sys.argv[5])
except:
	pass

threads = []
commands = []

class pixelsender(threading.Thread):
	def __init__(self, host, port):
		super(pixelsender, self).__init__()
	
	def addpixel(self):
		self.cmd = commands[:]
	
	def connect(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((host,port))

	def run(self):
		self.addpixel()
		random.shuffle(self.cmd)
		self.connect()
		subcmd = []
		while True:
			try:
				for elem in self.cmd:
					subcmd.append(elem)
					if len(subcmd) > 65*100:
						self.sock.sendall(b"".join(subcmd))
						subcmd = []
			except BrokenPipeError:
				sys.stdout.write('.')
				sys.stdout.flush()
				self.connect()
			except ConnectionResetError:
				time.sleep(5)
				self.connect()

img = Image.open(image)
(a, b, ix, iy) = img.getbbox()

random.seed()

def rnd(a):
	return random.randint(0,a)

def command_pixel(x, y, r, g, b):
	return 'PX {} {} {:02X}{:02X}{:02X}\n'.format(int(x), int(y), r, g, b).encode('UTF-8')

# send reuses a connection - higher speed for pixel
def getsize(s):
	s.sendall('SIZE\n'.encode('UTF-8'))
	msg = s.recv(64).decode('UTF-8')
	(_, xsize, ysize) = msg.strip().split()
	print('Size: {}x{} px'.format(xsize,ysize))
	return (int(xsize), int(ysize))

# Get the size of the image
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((host,port))
	(xstop, ystop) = getsize(s)

def addpixel():
	global xstart
	global ystart
	print('Img:  {}x{} px'.format(ix, iy))
	print('addpixel')
	if xstart == None or ystart == None:
		xstart = xstop/2 - ix/2
		ystart = ystop/2 - iy/2
	print('xstart: {}\nystart: {}'.format(xstart, ystart))
	for x in range(ix):
		for y in range(iy):
			(r, g, b) = img.getpixel((x,y))
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
