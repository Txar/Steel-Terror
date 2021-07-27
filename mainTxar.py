import pygame
from pygame.locals import *

playerxy = [0, 0]
height = 720
width = 1280
fps = 30
playerSpeed = 2 #tiles per second or smth idk
clock = pygame.time.Clock()
closeGame = False

pygame.init()
window = pygame.display.set_mode((width, height))

playerSprite = pygame.Surface((64, 64))
playerSprite.fill((255, 0, 0))
#this is temporary obviously

while True:
	if closeGame:
		break
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			closeGame = True
	keys = pygame.key.get_pressed()

	distanceToMove = playerSpeed/fps
	if keys[K_a]: playerxy[0] -= distanceToMove
	elif keys[K_d]: playerxy[0] += distanceToMove
	if keys[K_w]: playerxy[1] -= distanceToMove
	elif keys[K_s]: playerxy[1] += distanceToMove
	
	window.fill((0, 0, 0))
	pygame.draw.rect(window, (60, 60, 60), ((1024, 0), (256, 720))) #i think we might want this area of the screen for ui or smth?
	window.blit(playerSprite, (playerxy[0]*64, playerxy[1]*64))
	print(playerxy)
	pygame.display.update()
	clock.tick(fps)