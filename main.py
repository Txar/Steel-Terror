from pygame import *
from src.generation import *
from src.rendering import *
from src.logic import *
from random import *

mixer.pre_init(44100, -16, 2, 1024)
mixer.init()
beep = mixer.Sound("sfx/hit.wav")
bulletSound = mixer.Sound("sfx/bullet.wav")
bulletSound.set_volume(0.4)
hitSound = mixer.Sound("sfx/hit.wav")
hitSound.set_volume(0.4)
deathSound = mixer.Sound("sfx/enemyDeath.wav")
deathSound.set_volume(0.4)
eDeathSound = mixer.Sound("sfx/death.wav")
eDeathSound.set_volume(0.4)
selectSound = mixer.Sound("sfx/select.wav")
selectSound.set_volume(0.4)

init()
display.set_caption('Battle Big City')

screen, size, scw, sch, centerPos = loadScreen(20, 16)
forest, desert, ice, dungeon, tanks, enemyTanks, treads, bullet = loadImages()
ff = font.Font("fonts/font.ttf", size * 4)

fps = 60
clock = time.Clock()

playerSpeed = 2.5
playerxy = [0.5, 0.5, 0]
petxy = [0, 0, "none"] #none, duck, snek
health = 3
healthPacks = [] #[x, y]
ammoPacks = [] #[x, y]
rareLoot = [] #[x, y, what is it] things: 0 = fast tank, 1 = fat tank, 2 = duck, 3 = epic tank, 4 = snek
ammo = 50
bullets = [] #[bullet x, bullet y, bullet direction, bullet distance to move, 0 is player bullet 1 is enemy bullets]
enemies = [] #[x, y, direction, tank type, distance to move, ticks since the last shot, how many times travel the "distance to move", (if boss) max hp, (if boss) current hp]
enemiesToAdd = []#[type, if boss]
spawnCooldown = 120

tankStats = [0, [2.5, 4.5, 2.0, 0, 0], [3.7, 6.5, 2.7, 1, 0], [1.2, 5.5, 1.0, 2, 1], [3.1, 5.5, 0.8, 3, 1]] #tank type used currently, [speed, bullet speed, shooting cooldown, sprite, tracks sprite]

biomeDict = {
	1: forest,
	2: desert,
	3: ice,
	5: dungeon
}

mapSize = 20

mapList = generateMap(mapSize, 4)
diffMap = generateDiffMap(mapList, mapSize)
compMap = []

for i in range(mapSize):
	compMap.append([])
	for j in range(mapSize):
		if int(mapList[i][j]) == 0:
			compMap[i].append(1)
		else:
			compMap[i].append(0)

mapMap = []
for i in range(mapSize):
	mapMap.append([])
	for j in range(mapSize):
		jj = mapList[i][j]
		if jj == 0:
			f = open("rooms/0.water", "r")
			mapMap[i].append(renderRoom(f.read(), biomeDict[1]))
			f.close()
		elif jj == 4:
			f = open("rooms/{0}.shore".format(randint(0, 39)), "r")
			mapMap[i].append(renderRoom(f.read(), biomeDict[2]))
			f.close()
		else:
			f = open("rooms/{0}.room".format(randint(0, 39)), "r")
			mapMap[i].append(renderRoom(f.read(), biomeDict[jj]))
			f.close()

display.toggle_fullscreen()

mapPos = [10, 10]

data, waterData, bushData, blockData, breakableData, wholeRoomData, biome = mapMap[mapPos[0]][mapPos[1]]
enemiesToAdd = addEnemies(diffMap[mapPos[0]][mapPos[1]])

globals().update(locals())

menu = True
game = False
colors = False

colorList = [[1, 1, 2], [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [0.5, 0.2, 0.5], [0, 1, 1], [1, 1, 0], [1, 1, 1], [0.5, 0.5, 0.5]]
petList = ["none", "snek", "duck"]
tankList = ["default", "fast", "strong", "epic"]
lockedColors = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
lockedPets = [0, 1, 1]
lockedTanks = [0, 1, 1, 1]
t = 0
t2 = 0
deltaTime = 0
lastTicks = 0

bullet = surfaceImage(Image.open("sprites/tanks/bullet.png").resize((8 * size, 8 * size), Image.NONE))
enemyBullet = surfaceImage(Image.open("sprites/tanks/bullet1.png").resize((8 * size, 8 * size), Image.NONE))
heart = surfaceImage(Image.open("sprites/ui/heart.png").resize((4 * size, 4 * size), Image.NONE))
tank = surfaceImage(Image.open("sprites/ui/tank.png").resize((8 * size, 8 * size), Image.NONE))
buttSurface = surfaceNinepatch("sprites/ui/colorButton.9.png", 16, 9, size)
colorsButtonThing = surfaceNinepatch("sprites/ui/button.9.png", int(size * 10.8), int(size * 4.8), size)
colorsButtonThing2 = surfaceNinepatch("sprites/ui/button.9.png", int(size * 10.8), int(size * 2.8), size)
lock = surfaceImage(Image.open("sprites/ui/lock.png").resize((size * 8, size * 8), Image.NONE))
gLock = surfaceImage(Image.open("sprites/ui/goldenLock.png").resize((size * 8, size * 8), Image.NONE))

prevAmmo = 99999999999999999
cc = 0

mask = colorList[0]
screen.blit(Surface((scw, sch)), (0, 0))
for i in range(-1, 2):
	for j in range(-1, 2):
		if j == 0 and i == 0: continue
		blitSurround(screen, t, i * 20, j * 16, mapMap[mapPos[0] + i][mapPos[1] + j])
blitRoom(data, screen)
blitWater(waterData, screen, floor(t))
blitBlock(blockData, biome, screen)
blitBreakBlock(breakableData, biome, screen)
blitBush(bushData, biome, screen)
eeeeee = False
prevEnemies = -1
while 1:
	ee = event.get()

	if menu:
		play = button(screen, mouse, size, scw // 2, sch // 2 - 15 * size, 2, 2, "sprites/ui/button.9.png", "sprites/ui/buttonPressed.9.png", "sprites/ui/play.png")
		color = button(screen, mouse, size, scw // 2, sch // 2, 2, 2, "sprites/ui/button.9.png", "sprites/ui/buttonPressed.9.png", "sprites/ui/colors.png")
		#no #settings = button(screen, mouse, size, scw // 2, sch // 2 + 15 * size, 2, 2, "sprites/ui/button.9.png", "sprites/ui/buttonPressed.9.png", "sprites/ui/settings.png")

		u = 0
		for e in ee:
			if e.type == QUIT:
				quit()
				exit()
			if e.type == MOUSEBUTTONDOWN and play:
				beep.play()
				screen.blit(Surface((scw, sch)), (0, 0))
				for i in range(-1, 2):
					for j in range(-1, 2):
						if j == 0 and i == 0: continue
						blitSurround(screen, t, i * 20, j * 16, mapMap[mapPos[0] + i][mapPos[1] + j])
				blitRoom(data, screen)
				blitWater(waterData, screen, floor(t))
				blitBlock(blockData, biome, screen)
				blitBreakBlock(breakableData, biome, screen)
				blitBush(bushData, biome, screen)
				selectSound.play()
				menu = False
				game = True
			if e.type == MOUSEBUTTONDOWN and color:
				beep.play()
				screen.blit(Surface((scw, sch)), (0, 0))
				for i in range(-1, 2):
					for j in range(-1, 2):
						if j == 0 and i == 0: continue
						blitSurround(screen, t, i * 20, j * 16, mapMap[mapPos[0] + i][mapPos[1] + j])
				blitRoom(data, screen)
				blitWater(waterData, screen, floor(t))
				blitBlock(blockData, biome, screen)
				blitBreakBlock(breakableData, biome, screen)
				blitBush(bushData, biome, screen)
				selectSound.play()
				menu = False
				colors = True
				eeeeee = True

	if colors:
		screen.blit(colorsButtonThing, (scw // 2 - int(size * 22), sch // 2 - size * 12 - int(size * 10)))
		screen.blit(colorsButtonThing2, (scw // 2 - int(size * 22), sch // 2 - size * 12 + int(size * 20)))
		screen.blit(colorsButtonThing2, (scw // 2 - int(size * 22), sch // 2 - size * 12 + int(size * 40)))
		
		colorr = blitColors(screen, mouse, size, scw // 2 - int(size * 6 * 2.5), sch // 2 - size * 15, colorList, mask, lockedColors, lock)
		pett = blitPets(screen, mouse, size, scw // 2 - int(size * 6 * 2.5), sch // 2 + size * 15, petList, petxy[2], lockedPets, gLock)
		tankk = blitTankss(screen, mouse, size, scw // 2 - int(size * 6 * 2.5), sch // 2 + size * 35, tankList, tankList[tankStats[0]], lockedTanks, gLock)
		blitAmmo(screen, ammo, size, scw - 20 * size, size, ff, bullet, surfaceNinepatch("sprites/ui/colorButton.9.png", 11 + int(len(str(ammo)) * 2), 9, size))
		for e in ee:
			if e.type == QUIT:
				quit()
				exit()
			elif e.type == KEYDOWN:
				if e.key == K_ESCAPE:
					screen.blit(Surface((scw, sch)), (0, 0))
					for i in range(-1, 2):
						for j in range(-1, 2):
							if j == 0 and i == 0: continue
							blitSurround(screen, t, i * 20, j * 16, mapMap[mapPos[0] + i][mapPos[1] + j])
					blitRoom(data, screen)
					blitWater(waterData, screen, floor(t))
					blitBlock(blockData, biome, screen)
					blitBreakBlock(breakableData, biome, screen)
					blitBush(bushData, biome, screen)
					colors = False
					menu = True
			if e.type == MOUSEBUTTONDOWN and not eeeeee:
				if colorr != None:
					if not lockedColors[colorList.index(colorr)]:
						mask = colorr
					elif ammo >= 20:
						ammo -= 20
						mask = colorr
						lockedColors[colorList.index(colorr)] = 0
				if pett != None:
					if not lockedPets[petList.index(pett)]:
						petxy[2] = pett
					""" enable this to enable buying
					elif ammo >= 500:
						ammo -= 500
						petxy[2] = pett
						lockedPets[petList.index(pett)] = 0"""
				if tankk != None:
					if not lockedTanks[tankList.index(tankk)]:
						tankStats[0] = tankList.index(tankk)
		eeeeee = False

	if game:
		dd = len(bullets)
		playerSpeed, playerBulletSpeed, playerShootCooldown, tankSprite, tankTrackSprite = tankStats[int(tankStats[0])+1]
		if t2 < 999: t2 += 1
		for e in ee:
			if e.type == QUIT:
				quit()
				exit()
			elif e.type == KEYDOWN:
				if e.key == K_SPACE and t2 > fps*playerShootCooldown/2 and ammo > 0:
					t2 = 0
					spawnBullet(bullets, playerxy[0], playerxy[1], playerxy[2], playerBulletSpeed, fps, 0)
					ammo -= 1
				if e.key == K_f:
					spreadEnemy(enemies, wholeRoomData, randint(0, 3), playerxy)
				if e.key == K_ESCAPE and len(enemies) == 0 and len(enemiesToAdd) == 0:
					screen.blit(Surface((scw, sch)), (0, 0))
					for i in range(-1, 2):
						for j in range(-1, 2):
							if j == 0 and i == 0: continue
							blitSurround(screen, t, i * 20, j * 16, mapMap[mapPos[0] + i][mapPos[1] + j])
					blitRoom(data, screen)
					blitWater(waterData, screen, floor(t))
					blitBlock(blockData, biome, screen)
					blitBreakBlock(breakableData, biome, screen)
					blitBush(bushData, biome, screen)

					game = False
					menu = True

		if not game: continue
		keys = key.get_pressed()
		distanceToMove = playerSpeed * deltaTime
		uu = 0
		if keys[K_a]: playerxy[2], uu = 1, 1
		if keys[K_d] and not uu: playerxy[2], uu = 3, 1
		if keys[K_w] and not uu: playerxy[2], uu = 0, 1
		if keys[K_s] and not uu: playerxy[2], uu = 2, 1
		if not uu: distanceToMove = 0
		playerxy = checkPlayerCollisions(playerxy, distanceToMove, wholeRoomData, enemies)

		prevMapPos = mapPos
		if playerxy[0] < 0.5 and mapList[mapPos[0] - 1][mapPos[1]] != 0 and len(enemies) == 0 and len(enemiesToAdd) == 0:
			mapPos = [mapPos[0] - 1, mapPos[1]]
			playerxy[0] = 19.5
			cc = 1

		if playerxy[0] > 19.5 and mapList[mapPos[0] + 1][mapPos[1]] != 0 and len(enemies) == 0 and len(enemiesToAdd) == 0:
			mapPos = [mapPos[0] + 1, mapPos[1]]
			playerxy[0] = 0.5
			cc = 1

		if playerxy[1] < 0.5 and mapList[mapPos[0]][mapPos[1] - 1] != 0 and len(enemies) == 0 and len(enemiesToAdd) == 0:
			mapPos = [mapPos[0], mapPos[1] - 1]
			playerxy[1] = 15.5
			cc = 1

		if playerxy[1] > 15.5 and mapList[mapPos[0]][mapPos[1] + 1] != 0 and len(enemies) == 0 and len(enemiesToAdd) == 0:
			mapPos = [mapPos[0], mapPos[1] + 1]
			playerxy[1] = 0.5
			cc = 1

		if cc:
			compMap[prevMapPos[0]][prevMapPos[1]] = 1
			data, waterData, bushData, blockData, breakableData, wholeRoomData, biome = mapMap[mapPos[0]][mapPos[1]]
			if compMap[mapPos[0]][mapPos[1]] == 0:
				enemiesToAdd = addEnemies(diffMap[mapPos[0]][mapPos[1]])
			healthPacks = []
			ammoPacks = []
			cc = 0

		movePet(petxy, playerxy)
		bullets = moveBullets(bullets)
		health, ammo, healthPacks, ammoPacks = pickupPacks(health, ammo, healthPacks, ammoPacks, playerxy)
		bullets, wholeRoomData, breakableData, enemies, health, healthPacks, ammoPacks, rareLoot = checkBulletCollisions(hitSound, bullets, wholeRoomData, breakableData, playerxy, enemies, health, healthPacks, ammoPacks, rareLoot, lockedPets, lockedTanks)
		enemies, bullets = shootEnemies(enemies, bullets, wholeRoomData, tankStats, fps, playerxy)
		moveEnemies(enemies, wholeRoomData, fps, tankStats, playerxy)
		if spawnCooldown == 0:
			spawnCooldown = randint(60, 240)

			if(len(enemiesToAdd) <= 1): h = 0
			else: h = randint(0, len(enemiesToAdd) - 1)

			if len(enemiesToAdd) > 0:
				if len(enemiesToAdd[h]) > 0:
					if len(enemiesToAdd[h]) == 2: spreadEnemy(enemies, wholeRoomData, enemiesToAdd[h][0], enemiesToAdd[h][1], playerxy)
					else: spreadEnemy(enemies, wholeRoomData, enemiesToAdd[h][0], 0, playerxy)
				enemiesToAdd.pop(h)
			elif len(enemies) == 1 and enemies[0][-2] != 0: spreadEnemy(enemies, wholeRoomData, 2, 0, playerxy)
		else: spawnCooldown -= 1

		for i in range(-1, 2):
			for j in range(-1, 2):
				if j == 0 and i == 0: continue
				blitSurround(screen, t, i * 20, j * 16, mapMap[mapPos[0] + i][mapPos[1] + j])

		if len(bullets) < dd: bulletSound.play()

		blitRoom(data, screen)
		blitWater(waterData, screen, floor(t))
		blitPacks(healthPacks, ammoPacks, screen, heart, bullet)
		blitPlayer(playerxy, [tanks[tankSprite], treads[tankTrackSprite]], screen, t / 5, uu, mask)
		blitEnemies(enemies, screen, t, tankStats, [enemyTanks, treads])
		blitBullets(bullets, screen)
		blitBlock(blockData, biome, screen)
		blitBreakBlock(breakableData, biome, screen)
		blitBush(bushData, biome, screen)
		if len(enemies) + len(enemiesToAdd) != 0: blitFrame(screen, biome)
		blitHealthBars(enemies, screen)
		blitPet(petxy, playerxy, screen)

		if(ammo != prevAmmo):
			bulletButtSurface = surfaceNinepatch("sprites/ui/colorButton.9.png", 11 + int(len(str(ammo)) * 2), 9, size)

		if(len(enemies) < prevEnemies):
			deathSound.play()

		prevEnemies = len(enemies)
		blitHealth(screen, health, size, heart)
		blitAmmo(screen, ammo, size, scw - 20 * size, size, ff, bullet, bulletButtSurface)
		blitTanks(screen, len(enemiesToAdd) + len(enemies), size, scw - 40 * size, size, ff, tank, buttSurface)

		if health <= 0:
			game = False
			menu = True
			eDeathSound.play()
			ammo -= 100
			if ammo < 0:
				ammo = 0
			health = 3
			screen.blit(Surface((scw, sch)), (0, 0))
			for i in range(-1, 2):
				for j in range(-1, 2):
					if j == 0 and i == 0: continue
					blitSurround(screen, t, i * 20, j * 16, mapMap[mapPos[0] + i][mapPos[1] + j])
			blitRoom(data, screen)
			blitWater(waterData, screen, floor(t))
			blitBlock(blockData, biome, screen)
			blitBreakBlock(breakableData, biome, screen)
			blitBush(bushData, biome, screen)

		ti = time.get_ticks()
		deltaTime = (ti - lastTicks) / 1000
		lastTicks = ti

		prevAmmo = ammo

		t += deltaTime * 60
		t %= 360

	clock.tick(fps)
	display.update()
