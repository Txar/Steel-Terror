# This file cannot be run directly, use main.py instead
from PIL import Image
from math import *
from pygame import *
from random import *

global w, h, size, forest, water, screen, centerPos

def surfaceImage(pilImage):
	return image.fromstring(pilImage.tobytes(), pilImage.size, pilImage.mode).convert_alpha()

def split(word):
	return [char for char in word]

# a = value, ra = dimension, ts = tile size
def calculateSize(a, ra, ts):
	preValue = a
	value = a
	m = 0
	while 1:
		m += 1
		value -= ts * ra
		if value < 0:
			aa = preValue
			break
		preValue = value

	return m

# Load the initial data, returns the screen
def loadScreen(wd, hd):
	global w, h, size, centerPos
	w = wd
	h = hd

	infoObject = display.Info()
	scw, sch = infoObject.current_w, infoObject.current_h

	size = (min(calculateSize(scw, w, 2), calculateSize(sch - 50, h, 2)) - 1) * 2

	screen = display.set_mode((scw, sch), RESIZABLE)
	centerPos = (scw // 2 - (size * w) // 2, sch // 2 -(size * h) // 2)

	return screen

# Load all image data
def loadImages():
	global size, forest, water
	water = []
	forest = []

	for i in range(8):
		water.append(surfaceImage(Image.open("tiles/water/water" + str(i) + ".png").resize((size, size), Image.NONE)))

	for i in range(1, 5):
		forest.append(surfaceImage(Image.open("tiles/forest/" + str(i) + ".png").resize((size, size), Image.NONE)))

# Returns the image data of a room, and the position data of water tiles
def renderRoom(room):
	r = room.read()
	room.close()

	rr = r.split("\n")
	room = []

	for i in range(len(rr)):
		row = split(rr[i])
		room.append(row)

	data = []
	waterData = []
	idd = 0
	x = 0
	y = 0
	for i in room:
		data.append([])
		for q in i:
			j = int(q)
			if j == 0:
				data[idd].append(water[0])
				waterData.append([x, y])
			elif j == 1:
				data[idd].append(forest[0])
			elif j == 2:
				data[idd].append(forest[1])
			elif j == 3:
				data[idd].append(forest[2])
			elif j == 4:
				data[idd].append(forest[3])
			x += 1
		y += 1
		x = 0

		idd += 1

	return data, waterData

# Draw the room data into the screen
def blitRoom(data, screen):
	global centerPos
	for i in range(len(data) - 1):
		for j in range(len(data[0])):
			if data[i][j] == forest[3]:
				screen.blit(forest[0], (centerPos[0] + size * j, centerPos[1] + size * i))
			screen.blit(data[i][j], (centerPos[0] + size * j, centerPos[1] + size * i))

# Animate water with data as positions, t is ticks
def blitWater(waterData, screen, t):
	global size, centerPos
	for i in waterData:
		screen.blit(water[t % 8], (centerPos[0] + size * i[0], centerPos[1] + size * i[1]))
