import pygame
from pygame.locals import *
from src.rendering import *
from src.logic import *

init()

screen, size = loadScreen(20, 16)
forest, desert, ice, dungeon = loadImages()

fps = 60
clock = time.Clock()

playerSpeed = 2.5
playerxy = [0.5, 0.5, 0]

biome = dungeon
room = open("rooms/{0}.room".format(randint(0, 119)), "r")

data, waterData, bushData, breakableData, wholeRoomData = renderRoom(room, biome)

display.update()
t = 0
while 1:
	t %= 360
	ee = event.get()
	for e in ee:
		if e.type == QUIT:
			quit()
			exit()

	keys = pygame.key.get_pressed()
	distanceToMove = playerSpeed/fps
	uu = 0
	if keys[K_a]: playerxy[2], uu = 1, 1
	if keys[K_d] and not uu: playerxy[2], uu = 3, 1
	if keys[K_w] and not uu: playerxy[2], uu = 0, 1
	if keys[K_s] and not uu: playerxy[2], uu = 2, 1
	if not uu: distanceToMove = 0
	playerxy = checkPlayerCollisions(playerxy, distanceToMove, wholeRoomData)

	screen.blit(surfaceNinepatch("sprites/button.9.png", 32, 16, size), (40, 40))

	blitRoom(data, screen)

	blitPlayer(playerxy, 0, screen, t)# Tank rendering goes here
	
	blitWater(waterData, screen, floor(t))
	# Bullet rendering goes here
	blitBreakBlock(breakableData, biome, screen)
	blitBush(bushData, biome, screen)
	display.update()
	t += 1
	clock.tick(fps)
