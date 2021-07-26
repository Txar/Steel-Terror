# Generation by ThePythonGuy3
from math import *
from random import *
from perlin_noise import PerlinNoise
import os

def stringMap(l):
	o = ""
	for i in l:
		for j in i:
			o += str(j)
		o += "\n"

	return o

def printMap(l):
	print(stringMap(l))

def dist(x, y, x2, y2):
	return sqrt(abs(x - x2) ** 2 + abs(y - y2) ** 2)

def shore(x, y, w, h, mapList):
	if mapList[y][x] == 0:
		for i in range(-1, 2):
			for j in range(-1, 2):
				if y + i >= h or y + i < 0 or x + j >= w or x + j < 0: continue
				if mapList[y + i][x + j] != 0:
					return True
	return False

def copyMap(a):
	b = []
	p = -1
	for i in a:
		b.append([])
		p += 1
		for j in i:
			b[p].append(j)

	return b

"""
Codes:
0 - Ground
1 - Water
2 - Wall
3 - Breakable wall
4 - Bushes

Types:
shore - used in shores
water - used as sea
"""

def generateRoom(size = (20, 16), shore = False, water = False):
	w, h = size

	shoreAdd = int(shore) * 0.3

	room = []
	for i in range(h):
		room.append([])
		for j in range(w):
			room[i].append(0)

	# Creating tile noises
	wNoise = PerlinNoise(octaves = 10, seed = randint(1, 50))
	bwNoise = PerlinNoise(octaves = 10, seed = randint(1, 50))
	bNoise = PerlinNoise(octaves = 10, seed = randint(1, 50))
	wtNoise = PerlinNoise(octaves = 10, seed = randint(1, 50))

	# Full water tile
	default = 4
	if water: default = 1

	# Outer rim
	for i in range(h):
		for j in range(w):
			if bNoise([j / w, i / h]) >= 0.1:
				room[i][j] = default

	if water: return room

	# Inner room
	for i in range(1, h - 1):
		for j in range(1, w - 1):
			if wtNoise([j / w, i / h]) >= 0.3 - shoreAdd:
				room[i][j] = 1

			if wNoise([j / w, i / h]) >= 0.1:
				room[i][j] = 2

			if bwNoise([j / w, i / h]) >= 0.1:
				room[i][j] = 3

	return room

"""
Codes:
0 - Sea
1 - Plains
2 - Desert
3 - Ice
4 - Beach
5 - Dungeon
"""

def generateMap(size, dungeons):
	w = size
	h = size

	# Creating biome noises
	dNoise = PerlinNoise(octaves = 10, seed = randint(1, 50))
	iNoise = PerlinNoise(octaves = 10, seed = randint(1, 50))

	mapList = [] # x and y are inverted

	# Empty map (Default tiles)
	for i in range(h):
		mapList.append([])
		for j in range(w):
			mapList[i].append(1)

	# Map generation
	center = [floor(w / 2), floor(h / 2)]
	falloff = size // 2 - 3
	for i in range(h):
		for j in range(w):
			if dist(j, i, center[0], center[1]) >= falloff + randint(0, falloff // 3):
				mapList[i][j] = 0

			# Desert
			if abs(dNoise([j / w, i / h])) >= 0.2 and mapList[i][j] != 0:
				mapList[i][j] = 2

			# Ice
			if abs(iNoise([j / w, i / h])) >= 0.2 and mapList[i][j] != 0 and mapList[i][j] != 2:
				mapList[i][j] = 3

	# Dungeons
	for i in range(dungeons):
		while 1:
			x = randint(0, w - 1)
			y = randint(0, h - 1)

			if mapList[y][x] != 0:
				mapList[y][x] = 5
				break

	# Avoid list reassignment
	newMapList = copyMap(mapList)

	# Shores
	for i in range(h):
		for j in range(w):
			if shore(j, i, w, h, mapList):
				newMapList[i][j] = 4

	return newMapList

# One-time process, takes a long time
def generateRooms(dir = "rooms"):
	if not os.path.exists(dir):
		os.system("mkdir rooms")

	id = 0
	for i in range(120):
		f = open(dir + "/" + str(id) + ".room", "w+")

		f.write(stringMap(generateRoom()))

		f.close()
		id += 1

	id = 0
	for i in range(20):
		f = open(dir + "/" + str(id) + ".shore", "w+")

		f.write(stringMap(generateRoom(shore = True)))

		f.close()
		id += 1

	f = open(dir + "/" + "0.water", "w+")

	f.write(stringMap(generateRoom(water = True)))

printMap(generateMap(25, 4))
