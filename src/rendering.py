# This file cannot be run directly, use main.py instead
from PIL import Image
from math import *
from pygame import *
from random import *
from ninepatch import *

global w, h, size, forest, water, screen, centerPos

def surfaceImage(pilImage):
	return image.fromstring(pilImage.tobytes(), pilImage.size, pilImage.mode).convert_alpha()

def split(word):
	return [char for char in word]

# Make a surface out of a ninepatched surface (image url, output w/h, pixel scale)
def surfaceNinepatch(url, w, h, scale):
	np = Ninepatch(url)

	img = np.render(w, h)

	ww, hh = img.size
	img = img.resize((ww * scale, hh * scale), Image.NONE)

	return surfaceImage(img)

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

# Load the initial data, returns the screen and size scale
def loadScreen(wd, hd):
	global w, h, size, centerPos
	w = wd
	h = hd

	infoObject = display.Info()
	scw, sch = infoObject.current_w, infoObject.current_h

	size = (min(calculateSize(scw, w, 2), calculateSize(sch - 50, h, 2)) - 1) * 2

	screen = display.set_mode((scw, sch), RESIZABLE)
	centerPos = (scw // 2 - (size * w) // 2, sch // 2 -(size * h) // 2)

	return screen, size // 8

# Load all image data
def loadImages():
	global size, forest, water

	water = []

	forest = []
	desert = []
	ice = []
	dungeon = []

	for i in range(8):
		water.append(surfaceImage(Image.open("tiles/water/water" + str(i) + ".png").resize((size, size), Image.NONE)))

	for i in range(1, 5):
		forest.append(surfaceImage(Image.open("tiles/forest/" + str(i) + ".png").resize((size, size), Image.NONE)))
		desert.append(surfaceImage(Image.open("tiles/desert/" + str(i) + ".png").resize((size, size), Image.NONE)))
		ice.append(surfaceImage(Image.open("tiles/ice/" + str(i) + ".png").resize((size, size), Image.NONE)))
		dungeon.append(surfaceImage(Image.open("tiles/dungeon/" + str(i) + ".png").resize((size, size), Image.NONE)))

	return forest, desert, ice, dungeon


# Returns the image data of a room, and the position data of layers
def renderRoom(room, biome):
	r = room.read()
	room.close()

	rr = r.split("\n")
	room = []

	for i in range(len(rr)):
		row = split(rr[i])
		room.append(row)

	data = []
	waterData = []
	bushData = []
	breakableData = []
	idd = 0
	x = 0
	y = 0
	for i in room:
		data.append([])
		for q in i:
			j = int(q)
			if j == 0:
				data[idd].append(None)
				waterData.append([x, y])
			elif j == 1:
				data[idd].append(biome[0])
			elif j == 2:
				data[idd].append(biome[1])
			elif j == 3:
				data[idd].append(None)
				breakableData.append([x, y])
			elif j == 4:
				data[idd].append(None)
				bushData.append([x, y])
			x += 1
		y += 1
		x = 0

		idd += 1

	return data, waterData, bushData, breakableData

# Draw the room data into the screen
def blitRoom(data, screen):
	global centerPos
	for i in range(len(data) - 1):
		for j in range(len(data[0])):
			if data[i][j] == None: continue
			screen.blit(data[i][j], (centerPos[0] + size * j, centerPos[1] + size * i))

# Animate water with data as positions, t is ticks
def blitWater(waterData, screen, t):
	global size, centerPos
	for i in waterData:
		tt = int(min(((sin(radians(t)) + 1) / 2) * 33, 32))
		screen.blit(water[tt % 8], (centerPos[0] + size * i[0], centerPos[1] + size * i[1]))

def blitBush(bushData, biome, screen):
	global size, centerPos
	for i in bushData:
		screen.blit(biome[0], (centerPos[0] + size * i[0], centerPos[1] + size * i[1]))
		screen.blit(biome[3], (centerPos[0] + size * i[0], centerPos[1] + size * i[1]))

def blitBreakBlock(breakableData, biome, screen):
	global size, centerPos
	for i in breakableData:
		screen.blit(biome[2], (centerPos[0] + size * i[0], centerPos[1] + size * i[1]))