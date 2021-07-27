from src.rendering import *

init()

screen = loadScreen(20, 16)
loadImages()

room = open("rooms/{0}.room".format(randint(0, 119)), "r")

data, waterData = renderRoom(room)
blitRoom(data, screen)
display.update()

t = 0
while 1:
	event.get()
	blitWater(waterData, screen, floor(t))
	display.update()
	t += 0.01
