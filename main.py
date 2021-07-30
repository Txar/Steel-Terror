from pygame import *
#from pygame.locals import *
from src.rendering import *
from src.logic import *
from random import *

mixer.pre_init(44100, -16, 2, 1024)
mixer.init()
beep = mixer.Sound("sfx/hit.wav")
init()

screen, size, scw, sch = loadScreen(20, 16)
forest, desert, ice, dungeon, tanks, enemyTanks, treads, bullet = loadImages()
ff = font.Font("fonts/font.ttf", size * 4)

fps = 60
clock = time.Clock()

playerSpeed = 2.5
playerxy = [0.5, 0.5, 0]
petxy = [0, 0, "duck"]
health = 3
healthPacks = [] #[x, y]
ammoPacks = [] #[x, y]
ammo = 50
bullets = [] #[bullet x, bullet y, bullet direction, bullet distance to move, 0 is player bullet 1 is enemy bullets]
enemies = [] #[x, y, direction, tank type, distance to move, ticks since the last shot, how many times travel the "distance to move"]
tankStats = [1, [2.5, 4.5, 2.0, 0, 0], [3.7, 6.5, 2.7, 1, 0], [1.2, 5.5, 1.0, 2, 1], [3.1, 5.5, 0.8, 3, 1]] #tank type used currently, [speed, bullet speed, shooting cooldown, sprite, tracks sprite]

biome = forest
room = open("rooms/{0}.room".format(randint(0, 119)), "r")

display.toggle_fullscreen()

data, waterData, bushData, blockData, breakableData, wholeRoomData = renderRoom(room, biome)
spreadEnemy(enemies, wholeRoomData, 0, playerxy)

globals().update(locals())

menu = True
game = False
t = 0
t2 = 0
deltaTime = 0
lastTicks = 0

while 1:
	ee = event.get()

	if menu:
		play = button(screen, mouse, size, scw // 2, sch // 2 - 15 * size, 2, 2, "sprites/ui/button.9.png", "sprites/ui/buttonPressed.9.png", "sprites/ui/play.png")
		color = button(screen, mouse, size, scw // 2, sch // 2, 2, 2, "sprites/ui/button.9.png", "sprites/ui/buttonPressed.9.png", "sprites/ui/colors.png")
		settings = button(screen, mouse, size, scw // 2, sch // 2 + 15 * size, 2, 2, "sprites/ui/button.9.png", "sprites/ui/buttonPressed.9.png", "sprites/ui/settings.png")

		u = 0
		for e in ee:
			if e.type == QUIT:
				quit()
				exit()
			if e.type == MOUSEBUTTONDOWN and play:
				beep.play()
				screen.blit(Surface((scw, sch)), (0, 0))
				u = 1

		if u:
			menu = False
			game = True

	if game:
		playerSpeed, playerBulletSpeed, playerShootCooldown, tankSprite, tankTrackSprite = tankStats[int(tankStats[0])+1]
		if t2 < 999: t2 += 1
		for e in ee:
			if e.type == QUIT:
				quit()
				exit()
			elif e.type == KEYDOWN and e.key == K_SPACE and t2 > fps*playerShootCooldown/2 and ammo > 0:
				t2 = 0
				spawnBullet(bullets, playerxy[0], playerxy[1], playerxy[2], playerBulletSpeed, fps, 0)
				ammo -= 1
			elif e.type == KEYDOWN and e.key == K_f: spreadEnemy(enemies, wholeRoomData, randint(0, 3), playerxy)
		keys = key.get_pressed()
		distanceToMove = playerSpeed * deltaTime
		uu = 0
		if keys[K_a]: playerxy[2], uu = 1, 1
		if keys[K_d] and not uu: playerxy[2], uu = 3, 1
		if keys[K_w] and not uu: playerxy[2], uu = 0, 1
		if keys[K_s] and not uu: playerxy[2], uu = 2, 1
		if not uu: distanceToMove = 0
		playerxy = checkPlayerCollisions(playerxy, distanceToMove, wholeRoomData, enemies)
		movePet(petxy, playerxy)
		bullets = moveBullets(bullets)
		health, ammo, healthPacks, ammoPacks = pickupPacks(health, ammo, healthPacks, ammoPacks, playerxy)
		bullets, wholeRoomData, breakableData, enemies, health, healthPacks, ammoPacks = checkBulletCollisions(bullets, wholeRoomData, breakableData, playerxy, enemies, health, healthPacks, ammoPacks)
		enemies, bullets = shootEnemies(enemies, bullets, wholeRoomData, tankStats, fps, playerxy)
		moveEnemies(enemies, wholeRoomData, fps, tankStats, playerxy)
		blitRoom(data, screen)
		blitWater(waterData, screen, floor(t))
		blitPacks(healthPacks, ammoPacks, screen)
		blitPlayer(playerxy, [tanks[tankSprite], treads[tankTrackSprite]], screen, t / 5, uu)
		blitEnemies(enemies, screen, t, tankStats, [enemyTanks, treads])
		blitBullets(bullets, screen)
		blitBlock(blockData, biome, screen)
		blitBreakBlock(breakableData, biome, screen)
		blitBush(bushData, biome, screen)
		blitPet(petxy, screen)
		print(petxy)

		blitHealth(screen, health, size)
		blitAmmo(screen, ammo, size, scw - 120, 5, ff)

		ti = time.get_ticks()
		deltaTime = (ti - lastTicks) / 1000
		lastTicks = ti

		t += deltaTime * 60
		t %= 360

	clock.tick(fps)
	display.update()
