from pygame import *
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
playerBulletSpeed = 4.5
playerShootCooldown = 1.5
bullets = [] #[bullet x, bullet y, bullet direction, bullet distance to move]
tankStats = [0, [2.5, 4.5, 1.5, 0, 0], [3.7, 4.5, 2.7, 1, 0], [1.2, 5.5, 1.0, 2, 1], [3.1, 5.5, 0.8, 2, 1]] #tank type used currently, [speed, bullet speed, shooting cooldown, sprite, tracks sprite]

biome = desert
room = open("rooms/{0}.room".format(randint(0, 119)), "r")

display.toggle_fullscreen()

data, waterData, bushData, breakableData, wholeRoomData = renderRoom(room, biome)

lastTicks = 0

while 1:
	ee = event.get()

	aaaa = button(screen, mouse, size, 40, 40, 2, 2, "sprites/ui/button.9.png", "sprites/ui/buttonPressed.9.png", "sprites/ui/play.png")

	for e in ee:
		if e.type == QUIT:
			quit()
			exit()
		if e.type == MOUSEBUTTONDOWN and aaaa:
			print("no")

	display.update()

t = 0
t2 = 0
while 1:
	playerSpeed, playerBulletSpeed, playerShootCooldown, tankSprite, tankTrackSprite = tankStats[int(tankStats[0])+1]
	t2 += 1
	ee = event.get()
	for e in ee:
		if e.type == QUIT:
			quit()
			exit()
		elif e.type == KEYDOWN and e.key == K_SPACE and t2 > fps*playerShootCooldown/2:
			t2 = 0
			spawnBullet(bullets, playerxy[0], playerxy[1], playerxy[2], playerBulletSpeed, fps)
	keys = key.get_pressed()
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

	blitRoom(data, screen)

	blitPlayer(playerxy, [tanks[tankSprite], treads[tankTrackSprite]], screen, t / 5, uu)

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