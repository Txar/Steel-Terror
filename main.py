import pygame
from pygame.locals import *
from src.rendering import *
from src.logic import *

init()

screen, size = loadScreen(20, 16)
forest, desert, ice, dungeon, tanks, treads, bullet = loadImages()

fps = 60
clock = time.Clock()

playerSpeed = 2.5
playerBulletSpeed = 3.5
playerxy = [0.5, 0.5, 0]
bullets = [] #[bullet x, bullet y, bullet direction, bullet distance to move]

biome = desert
room = open("rooms/{0}.room".format(randint(0, 119)), "r")

data, waterData, bushData, breakableData, wholeRoomData = renderRoom(room, biome)

lastTicks = 0

display.update()
t = 0
while 1:
	ee = event.get()
	for e in ee:
		if e.type == QUIT:
			#quit()
			#exit()
			fps = 30
		elif e.type == pygame.KEYDOWN and e.key == K_SPACE: spawnBullet(bullets, playerxy[0], playerxy[1], playerxy[2], playerBulletSpeed, fps)

	keys = pygame.key.get_pressed()
	distanceToMove = playerSpeed/fps
	uu = 0
	if keys[K_a]: playerxy[2], uu = 1, 1
	if keys[K_d] and not uu: playerxy[2], uu = 3, 1
	if keys[K_w] and not uu: playerxy[2], uu = 0, 1
	if keys[K_s] and not uu: playerxy[2], uu = 2, 1
	if not uu: distanceToMove = 0
	playerxy = checkPlayerCollisions(playerxy, distanceToMove, wholeRoomData)
	bullets = moveBullets(bullets)
	bullets, wholeRoomData, breakableData = checkBulletCollisions(bullets, wholeRoomData, breakableData)

	screen.blit(surfaceNinepatch("sprites/ui/button.9.png", 32, 16, size), (40, 40))

	blitRoom(data, screen)

	blitPlayer(playerxy, [tanks[3], treads[0]], screen, t / 5, uu)
	
	blitWater(waterData, screen, floor(t))
	
	blitBullets(bullets, screen)# Bullet rendering goes here
	
	blitBreakBlock(breakableData, biome, screen)
	blitBush(bushData, biome, screen)

	ti = time.get_ticks()
	deltaTime = (ti - lastTicks) / 1000
	lastTicks = ti

	display.update()
	t += deltaTime * 60
	t %= 360


	clock.tick(fps)