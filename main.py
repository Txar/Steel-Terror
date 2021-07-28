from pygame import *
#from pygame.locals import *
from src.rendering import *
from src.logic import *

init()

# Oh boy globals
global screen, size, scw, sch, forest, desert, ice, dungeon, tanks, treads, bullet, fps, clock
global playerxy, health, ammo, player, bullets, enemies, tankStats
global biome, room, data, waterData, bushData, breakableData, wholeRoomData
screen, size, scw, sch = loadScreen(20, 16)
forest, desert, ice, dungeon, tanks, treads, bullet = loadImages()

fps = 60
clock = time.Clock()

playerSpeed = 2.5
playerxy = [0.5, 0.5, 0]
health = 3
ammo = 50
bullets = [] #[bullet x, bullet y, bullet direction, bullet distance to move]
enemies = [] #[x, y, direction, tank type, distance to move, ticks since the last shot, how many times travel the "distance to move"]
tankStats = [0, [2.5, 4.5, 1.5, 0, 0], [3.7, 4.5, 2.7, 1, 0], [1.2, 5.5, 1.0, 2, 1], [3.1, 5.5, 0.8, 3, 1]] #tank type used currently, [speed, bullet speed, shooting cooldown, sprite, tracks sprite]

biome = dungeon
room = open("rooms/{0}.room".format(randint(0, 119)), "r")

display.toggle_fullscreen()

data, waterData, bushData, breakableData, wholeRoomData = renderRoom(room, biome)
spreadEnemy(enemies, wholeRoomData, 0)

globals().update(locals())

def menu():
	while 1:
		ee = event.get()

		play = button(screen, mouse, size, scw // 2, sch // 2 - 15 * size, 2, 2, "sprites/ui/button.9.png", "sprites/ui/buttonPressed.9.png", "sprites/ui/play.png")
		color = button(screen, mouse, size, scw // 2, sch // 2, 2, 2, "sprites/ui/button.9.png", "sprites/ui/buttonPressed.9.png", "sprites/ui/colors.png")
		settings = button(screen, mouse, size, scw // 2, sch // 2 + 15 * size, 2, 2, "sprites/ui/button.9.png", "sprites/ui/buttonPressed.9.png", "sprites/ui/settings.png")

		u = 0
		for e in ee:
			if e.type == QUIT:
				quit()
				exit()
			if e.type == MOUSEBUTTONDOWN and play:
				screen.blit(Surface((scw, sch)), (0, 0))
				u = 1

		if u:
			# Workaround for code after return, pretty big brain
			try:
				return
			finally:
				playee()

		display.update()
		clock.tick(fps)

def playee():
	# OMG im so sorry, but python has no gotos so this is the only way :(
	global screen, size, scw, sch, forest, desert, ice, dungeon, tanks, treads, bullet, fps, clock
	global playerxy, health, ammo, player, bullets, enemies, tankStats
	global biome, room, data, waterData, bushData, breakableData, wholeRoomData

	t = 0
	t2 = 0
	deltaTime = 0
	lastTicks = 0

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
				spreadEnemy(enemies, wholeRoomData, 3)
		keys = key.get_pressed()
		distanceToMove = playerSpeed * deltaTime
		uu = 0
		if keys[K_a]: playerxy[2], uu = 1, 1
		if keys[K_d] and not uu: playerxy[2], uu = 3, 1
		if keys[K_w] and not uu: playerxy[2], uu = 0, 1
		if keys[K_s] and not uu: playerxy[2], uu = 2, 1
		if not uu: distanceToMove = 0
		playerxy = checkPlayerCollisions(playerxy, distanceToMove, wholeRoomData)
		bullets = moveBullets(bullets)
		bullets, wholeRoomData, breakableData = checkBulletCollisions(bullets, wholeRoomData, breakableData)
		enemies, bullets = shootEnemies(enemies, bullets, wholeRoomData, tankStats, fps, playerxy)

		blitRoom(data, screen)
		blitWater(waterData, screen, floor(t))

		blitPlayer(playerxy, [tanks[tankSprite], treads[tankTrackSprite]], screen, t / 5, uu)
		blitEnemies(enemies, screen, t, tankStats, [tanks, treads])

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

menu()