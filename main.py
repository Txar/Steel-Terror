from src.rendering import *

init()

screen, size = loadScreen(20, 16)
forest, desert, ice, dungeon = loadImages()

fps = 60
clock = time.Clock()

biome = dungeon
room = open("rooms/{0}.room".format(randint(0, 119)), "r")

data, waterData, bushData, breakableData = renderRoom(room, biome)

display.update()

t = 0
while 1:
	ee = event.get()
	for e in ee:
		if e.type == QUIT:
			quit()
			exit()

	screen.blit(surfaceNinepatch("sprites/button.9.png", 32, 16, size), (40, 40))

	blitRoom(data, screen)
	# Tank rendering goes here
	blitWater(waterData, screen, floor(t))
	# Bullet rendering goes here
	blitBreakBlock(breakableData, biome, screen)
	blitBush(bushData, biome, screen)

	display.update()
	t += 1
	clock.tick(fps)
