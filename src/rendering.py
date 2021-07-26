from PIL import Image
from math import *
from pygame import *

water = []
forest = []

def pilImageToSurface(pilImage):
	return image.fromstring(pilImage.tobytes(), pilImage.size, pilImage.mode).convert_alpha()

def split(word):
	return [char for char in word]

init()

size = 16

w = 20
h = 16

screen = display.set_mode((size * w, size * h))
surface = Surface((size * w, size * h))

for i in range(8):
	water.append(pilImageToSurface(Image.open("../tiles/water/water" + str(i) + ".png").resize((size, size), Image.NONE)))

for i in range(1, 5):
	forest.append(pilImageToSurface(Image.open("../tiles/forest/" + str(i) + ".png").resize((size, size), Image.NONE)))

room = open("../rooms/0.room", "r")

def renderRoom(room):
	r = room.read()
	room.close()

	rr = r.split("\n")
	room = []

	for i in range(len(rr)):
		row = split(rr[i])
		room.append(row)

	data = []
	idd = 0
	for i in room:
		data.append([])
		for q in i:
			j = int(q)
			if j == 0:
				data[idd].append(water[0])
			elif j == 1:
				data[idd].append(forest[0])
			elif j == 2:
				data[idd].append(forest[1])
			elif j == 3:
				data[idd].append(forest[2])
			elif j == 4:
				data[idd].append(forest[3])
		idd += 1

	return data

def blitRoom(data, screen):
	for i in range(len(data) - 1):
		for j in range(len(data[0])):
			if data[i][j] == forest[3]:
				screen.blit(forest[0], (size * j, size * i))
			screen.blit(data[i][j], (size * j, size * i))

blitRoom(renderRoom(room), screen)
display.update()

while 1:
	event.get()

