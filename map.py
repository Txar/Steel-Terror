from math import *
from random import *
from perlin_noise import PerlinNoise
import os

tiles = os.listdir("map")

def printMap(l):
	for i in l:
		o = ""
		for j in i:
			o += str(j)
		print(o)

def dist(x, y, x2, y2):
	return sqrt(abs(x - x2) ** 2 + abs(y - y2) ** 2)

"""
Codes:
0 - Sea
1 - Plains
2 - Desert
3 - Ice
4 - Dungeon
"""

def generateMap(size, dungeons):
	w = size
	h = size

	# Generating biome noises
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
	for i in range(len(mapList)):
		for j in range(len(mapList[i])):
			if(dist(j, i, center[0], center[1]) >= falloff + randint(0, falloff // 3)):
				mapList[i][j] = 0

			# Desert
			if(abs(dNoise([j / w, i / h])) >= 0.2 and mapList[i][j] != 0):
				mapList[i][j] = 2

			# Ice
			if(abs(iNoise([j / w, i / h])) >= 0.2 and mapList[i][j] != 0 and mapList[i][j] != 2):
				mapList[i][j] = 3

	# Dungeons
	for i in range(dungeons):
		while 1:
			x = randint(0, w - 1)
			y = randint(0, h - 1)

			if(mapList[y][x] != 0):
				mapList[y][x] = 4
				break


	return mapList

printMap(generateMap(25, 4))