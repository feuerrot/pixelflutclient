#!/usr/bin/env python3
import random
import socket
import sys
import threading
import time
from PIL import Image

NUMOFTHREADS = 8
ALPHA = 0

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
	sip = str(sys.argv[4])
except:
	sip = None

try:
	x = int(sys.argv[5])
	y = int(sys.argv[6])
	xstart = x
	ystart = y
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
		if sip != None:
			self.sock.bind((sip, 0))
		while True:
			try:
				self.sock.connect((host,port))
				break
			except TimeoutError:
				sys.stdout.write('T')
				sys.stdout.flush()
				time.sleep(1)
		sys.stdout.write('c')
		sys.stdout.flush()

	def run(self):
		self.addpixel()
		random.shuffle(self.cmd)
		self.connect()
		subcmd = []
		while True:
			try:
				for elem in self.cmd:
					subcmd.append(elem)
					if len(subcmd) > 2**10:
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
	size = msg.strip().split()
	print(len(size))
	if len(size) == 2:
		(xsize, ysize) = size
	elif len(size) == 3:
		(_, xsize, ysize) = size
	elif len(size) == 4:
		(_, xsize, ysize, _) = size
	print('Size: {}x{} px'.format(xsize,ysize))
	return (int(xsize), int(ysize))

# Get the size of the image
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	if sip != None:
		s.bind((sip, 0))
	s.connect((host,port))
	(xstop, ystop) = getsize(s)

def addpixel():
	global xstart
	global ystart
	print('Img:  {}x{} px'.format(ix, iy))
	print('addpixel')
	if xstart == None or ystart == None:
		xstart = xstop - ix
		ystart = ystop - iy
	print('xstart: {}\nystart: {}'.format(xstart, ystart))
	for x in range(ix):
		for y in range(iy):
			(r, g, b) = img.getpixel((x,y))
			if ALPHA - 2 <= r and r <= ALPHA + 2 and ALPHA - 2 <= g and g <= ALPHA + 2 and ALPHA - 2 <= b and b <= ALPHA + 2:
				continue
			commands.append(command_pixel(x+xstart, y+ystart, r, g, b))
	print('addedpixels')

try:
	addpixel()
	for _ in range(NUMOFTHREADS):
		threads.append(pixelsender(host, port))
		sys.stdout.write('t')
		sys.stdout.flush()

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
