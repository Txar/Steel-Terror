import pygame
from pygame.locals import *
from src.rendering import *

init()

screen, size = loadScreen(20, 16)
forest, desert, ice, dungeon = loadImages()

fps = 60
clock = time.Clock()

playerSpeed = 1
playerxy = [0, 0, 0]

biome = dungeon
room = open("rooms/{0}.room".format(randint(0, 119)), "r")

data, waterData, bushData, breakableData = renderRoom(room, biome)
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
	uu = 1
	if keys[K_a]: playerxy[0], playerxy[2], uu = playerxy[0] - distanceToMove, 1, 0
	if keys[K_d] and uu: playerxy[0], playerxy[2], uu = playerxy[0] + distanceToMove, 3, 0
	if keys[K_w] and uu: playerxy[1], playerxy[2], uu = playerxy[1] - distanceToMove, 0, 0
	if keys[K_s] and uu: playerxy[1], playerxy[2] = playerxy[1] + distanceToMove, 2

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
