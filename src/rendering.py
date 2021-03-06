# This file cannot be run directly, use main.py instead
from PIL import Image, ImageOps
from math import *
from pygame import *
from random import *
from ninepatch import *

global w, h, size, forest, water, screen, centerPos

def surfaceImage(pilImage):
	return image.fromstring(pilImage.tobytes(), pilImage.size, pilImage.mode).convert_alpha()

def split(word):
	return [char for char in word]

# Make a surface out of a ninepatched surface (image url, output w/h, pixel scale)
def surfaceNinepatch(url, w, h, scale):
	np = Ninepatch(url)

	img = np.render(w, h)

	ww, hh = img.size
	img = img.resize((ww * scale, hh * scale), Image.NONE)

	return surfaceImage(img)

"""
screen
mouse
size
button x
buttony
text image offset x
text image offset y
button image url
hovered button image url
text image url
action (lambda)
"""
def button(screen, m, size, x, y, ox, oy, burl, pburl, turl):
	text = Image.open(turl)
	ww, hh = text.size
	mx, my = m.get_pos()

	w = ox * 2 + ww
	h = oy * 2 + hh

	a = False
	if mx >= x  - (w // 2) * size and mx <= x + w * size  - (w // 2) * size and my >= y - (h // 2) * size and my <= y + h * size - (h // 2) * size:
		screen.blit(surfaceNinepatch(pburl, w, h, size), (x - (w // 2) * size, y - (h // 2) * size))
		a = True
	else:
		screen.blit(surfaceNinepatch(burl, w, h, size), (x - (w // 2) * size, y - (h // 2) * size))

	screen.blit(surfaceImage(text.resize((size * ww, size * hh), Image.NONE)), (x + size * ox - (w // 2) * size, y + size * oy - (h // 2) * size))

	return a

def colorButton(screen, m, size, x, y, color, lit):
	w, h = 8, 8
	mx, my = m.get_pos()

	if lit:
		screen.blit(applyMask(surfaceImage(Image.open("sprites/ui/colorButtonPressed.png").resize((w * size, h * size), Image.NONE)), color, w * size), (x - (w // 2) * size, y - (h // 2) * size))
	else:
		screen.blit(applyMask(surfaceImage(Image.open("sprites/ui/colorButton.png").resize((w * size, h * size), Image.NONE)), color, w * size), (x - (w // 2) * size, y - (h // 2) * size))

	if mx >= x  - (w // 2) * size and mx <= x + w * size  - (w // 2) * size and my >= y - (h // 2) * size and my <= y + h * size - (h // 2) * size:
		return color

	return None

def petButton(screen, m, size, x, y, pet, lit):
	w, h = 10, 10
	mx, my = m.get_pos()

	if lit:
		screen.blit(surfaceImage(Image.open("sprites/ui/petHighlight.png").resize((w * size, h * size), Image.NONE)), (x - (w // 2) * size, y - (h // 2) * size))

	screen.blit(surfaceImage(Image.open("sprites/pets/" + pet + "0.png").resize((8 * size, 8 * size), Image.NONE)), (x - (8 // 2) * size, y - (8 // 2) * size))

	if mx >= x  - (w // 2) * size and mx <= x + w * size  - (w // 2) * size and my >= y - (h // 2) * size and my <= y + h * size - (h // 2) * size:
		return pet

	return None

def tankButton(screen, m, size, x, y, tank, lit):
	w, h = 10, 10
	mx, my = m.get_pos()

	if lit:
		screen.blit(surfaceImage(Image.open("sprites/ui/petHighlight.png").resize((w * size, h * size), Image.NONE)), (x - (w // 2) * size, y - (h // 2) * size))

	screen.blit(surfaceImage(Image.open("sprites/tanks/" + tank + "/display.png").resize((8 * size, 8 * size), Image.NONE)), (x - (8 // 2) * size, y - (8 // 2) * size))

	if mx >= x  - (w // 2) * size and mx <= x + w * size  - (w // 2) * size and my >= y - (h // 2) * size and my <= y + h * size - (h // 2) * size:
		return tank

	return None

def blitColors(screen, m, size, x, y, colorList, color, lockedColors, lock):
	xx = 0
	yy = 0
	o = None
	ii = 0
	for i in colorList:
		value = colorButton(screen, m, size, xx + x, yy + y, i, color == i)
		if lockedColors[ii]: screen.blit(lock, (xx + x - size * 4, yy + y - size * 4))
		if value != None and o == None:
			o = value
		xx += 10 * size
		if xx >= 50 * size:
			xx = 0
			yy += 10 * size
		ii += 1
	return o

def blitPets(screen, m, size, x, y, petList, pet, lockedPets, lock):
	xx = 0
	yy = 0
	o = None
	ii = 0
	for i in petList:
		value = petButton(screen, m, size, xx + x, yy + y, i, pet == i)
		if lockedPets[ii]: screen.blit(lock, (xx + x - size * 4, yy + y - size * 4))
		if value != None and o == None:
			o = value
		xx += 10 * size
		if xx >= 50 * size:
			xx = 0
			yy += 10 * size
		ii += 1
	return o

def blitTankss(screen, m, size, x, y, tankList, tank, lockedTanks, lock):
	xx = 0
	yy = 0
	o = None
	ii = 0
	for i in tankList:
		value = tankButton(screen, m, size, xx + x, yy + y, i, tank == i)
		if lockedTanks[ii]: screen.blit(lock, (xx + x - size * 4, yy + y - size * 4))
		if value != None and o == None:
			o = value
		xx += 10 * size
		if xx >= 50 * size:
			xx = 0
			yy += 10 * size
		ii += 1
	return o

def blitHealth(screen, health, size, heart):
	x = 3 / 5
	y = 0.4
	for i in range(health):
		screen.blit(heart, (int(x * size * 5), int(y * size * 5)))
		x += 1
		if x > 8:
			x = 3 / 5
			y += 1

def blitAmmo(screen, ammo, size, x, y, f, bullet, buttSurface):
	textSurface = f.render("x" + str(ammo), False, (0, 0, 0))

	screen.blit(buttSurface, (x + size, y))
	screen.blit(bullet, (x, y))
	screen.blit(textSurface, (x + 6 * size, y + 3 * size))

def blitTanks(screen, tanks, size, x, y, f, tank, buttSurface):
	textSurface = f.render("x" + str(tanks), False, (0, 0, 0))

	screen.blit(buttSurface, (x, y))
	screen.blit(tank, (x, y))
	screen.blit(textSurface, (x + 7 * size, y + 3 * size))

# a = value, ra = dimension, ts = tile size
def calculateSize(a, ra, ts):
	preValue = a
	value = a
	m = 0
	while 1:
		m += 1
		value -= ts * ra
		if value < 0:
			aa = preValue
			break
		preValue = value

	return m

def applyMask(surface, colorMult, size):
	newSurf = Surface((size, size), SRCALPHA, 32)
	for i in range(size):
		for j in range(size):
			r1, g1, b1, a = surface.get_at((i, j))
			pix = [0, 0, 0]
			r, g, b = colorMult
			if a != 0:
				r1 *= r
				g1 *= g
				b1 *= b
				pix[0] = min(r1, 255)
				pix[1] = min(g1, 255)
				pix[2] = min(b1, 255)
				newSurf.set_at((i, j), pix)
	return newSurf

# Load the initial data, returns the screen and size scale
def loadScreen(wd, hd):
	global w, h, size, centerPos
	w = wd
	h = hd

	infoObject = display.Info()
	scw, sch = infoObject.current_w, infoObject.current_h

	size = (min(calculateSize(scw, w, 2), calculateSize(sch - 50, h, 2)) - 1) * 2

	screen = display.set_mode((scw, sch), RESIZABLE)
	centerPos = (scw // 2 - (size * w) // 2, sch // 2 -(size * h) // 2)

	return screen, size // 8, scw, sch, centerPos

# Load all image data
def loadImages():
	global size, forest, ice, dungeon, desert, water, tanks, bullet, duck0, duck1, none0, none1, snek0, snek1, healthBar, enemyBullet, boss, goldenUnlock

	water = []

	forest = []
	desert = []
	ice = []
	dungeon = []

	tanks = []
	enemyTanks = []
	tankTypes = ["default", "fast", "strong", "epic"]

	treads = []

	for i in range(8):
		water.append(surfaceImage(Image.open("tiles/water/water" + str(i) + ".png").resize((size, size), Image.NONE)))

	for i in range(1, 5):
		forest.append(surfaceImage(Image.open("tiles/forest/" + str(i) + ".png").resize((size, size), Image.NONE)))
		desert.append(surfaceImage(Image.open("tiles/desert/" + str(i) + ".png").resize((size, size), Image.NONE)))
		ice.append(surfaceImage(Image.open("tiles/ice/" + str(i) + ".png").resize((size, size), Image.NONE)))
		dungeon.append(surfaceImage(Image.open("tiles/dungeon/" + str(i) + ".png").resize((size, size), Image.NONE)))

	# up, right, down, left
	ii = 0
	for i in tankTypes:
		enemyTanks.append([])
		enemyTanks[ii].append(applyMask(surfaceImage(Image.open("sprites/tanks/" + i + "/0.png").resize((size, size), Image.NONE)), [2, 1, 1], size))
		enemyTanks[ii].append(applyMask(surfaceImage(ImageOps.mirror(Image.open("sprites/tanks/" + i + "/1.png").resize((size, size), Image.NONE))), [2, 1, 1], size))
		enemyTanks[ii].append(applyMask(surfaceImage(ImageOps.flip(Image.open("sprites/tanks/" + i + "/0.png").resize((size, size), Image.NONE))), [2, 1, 1], size))
		enemyTanks[ii].append(applyMask(surfaceImage(Image.open("sprites/tanks/" + i + "/1.png").resize((size, size), Image.NONE)), [2, 1, 1], size))
		ii += 1
	ii = 0
	for i in tankTypes:
		tanks.append([])
		tanks[ii].append(surfaceImage(Image.open("sprites/tanks/" + i + "/0.png").resize((size, size), Image.NONE)))
		tanks[ii].append(surfaceImage(ImageOps.mirror(Image.open("sprites/tanks/" + i + "/1.png").resize((size, size), Image.NONE))))
		tanks[ii].append(surfaceImage(ImageOps.flip(Image.open("sprites/tanks/" + i + "/0.png").resize((size, size), Image.NONE))))
		tanks[ii].append(surfaceImage(Image.open("sprites/tanks/" + i + "/1.png").resize((size, size), Image.NONE)))
		ii += 1

	boss = []
	bossColor = [2, 1, 0]
	boss.append(applyMask(surfaceImage(Image.open("sprites/tanks/epic/0.png").resize((size, size), Image.NONE)), bossColor, size))
	boss.append(applyMask(surfaceImage(ImageOps.mirror(Image.open("sprites/tanks/epic/1.png").resize((size, size), Image.NONE))), bossColor, size))
	boss.append(applyMask(surfaceImage(ImageOps.flip(Image.open("sprites/tanks/epic/0.png").resize((size, size), Image.NONE))), bossColor, size))
	boss.append(applyMask(surfaceImage(Image.open("sprites/tanks/epic/1.png").resize((size, size), Image.NONE)), bossColor, size))

	for i in range(1, 3):
		treads.append([])
		for j in range(1, 3):
			treads[i - 1].append(surfaceImage(Image.open("sprites/tanks/treads/tread" + str(i) + str(j) +".png").resize((size, size), Image.NONE)))

	healthBar = []
	for i in range(0, 14):
		healthBar.append(surfaceImage(Image.open("sprites/ui/healthbar" + str(i) + ".png").resize((size * 2, size), Image.NONE)))

	bullet = surfaceImage(Image.open("sprites/tanks/bullet1.png").resize((size, size), Image.NONE))
	enemyBullet = surfaceImage(Image.open("sprites/tanks/bullet.png").resize((size, size), Image.NONE))
	duck0 = surfaceImage(Image.open("sprites/pets/duck0.png").resize((size, size), Image.NONE))
	duck1 = surfaceImage(Image.open("sprites/pets/duck1.png").resize((size, size), Image.NONE))
	none0 = Surface((size, size), SRCALPHA)
	none1 = Surface((size, size), SRCALPHA)
	snek0 = surfaceImage(Image.open("sprites/pets/snek0.png").resize((size, size), Image.NONE))
	snek1 = surfaceImage(Image.open("sprites/pets/snek1.png").resize((size, size), Image.NONE))
	goldenUnlock = surfaceImage(Image.open("sprites/ui/goldenUnlock.png").resize((int(size * 1.5), int(size * 1.5)), Image.NONE))

	return forest, desert, ice, dungeon, tanks, enemyTanks, treads, bullet


# Returns the image data of a room, and the position data of layers
def renderRoom(r, biome):
	rr = r.split("\n")
	room = []

	for i in range(len(rr)):
		row = split(rr[i])
		room.append(row)

	data = []
	waterData = []
	bushData = []
	blockData = []
	breakableData = []
	idd = 0
	x = 0
	y = 0
	for i in room:
		data.append([])
		for q in i:
			j = int(q)
			if j == 0:
				data[idd].append(None)
				waterData.append([x, y])
			elif j == 1:
				data[idd].append(biome[0])
			elif j == 2:
				data[idd].append(None)
				blockData.append([x, y])
			elif j == 3:
				data[idd].append(biome[0])
				breakableData.append([x, y])
			elif j == 4:
				data[idd].append(biome[0])
				bushData.append([x, y])
			x += 1
		y += 1
		x = 0

		idd += 1

	return data, waterData, bushData, blockData, breakableData, room, biome

# Draw the room data into the screen
def blitRoom(data, screen, ox = 0, oy = 0):
	global centerPos
	for i in range(len(data) - 1):
		for j in range(len(data[0])):
			if data[i][j] == None: continue
			screen.blit(data[i][j], (centerPos[0] + size * j + ox * size, centerPos[1] + size * i + oy * size))

def blitFrame(screen, biome):
	global size, centerPos
	for i in range(-1, 21):
		for j in range(-1, 17):
			if j == -1 or j == 16 or i == -1 or i == 20:
				screen.blit(biome[1], (centerPos[0] + size * i, centerPos[1] + size * j))

# Animate water with data as positions, t is ticks
def blitWater(waterData, screen, t, ox = 0, oy = 0):
	global size, centerPos
	for i in waterData:
		tt = int(min(((sin(radians(t)) + 1) / 2) * 33, 32))
		screen.blit(water[tt % 8], (centerPos[0] + size * i[0] + ox * size, centerPos[1] + size * i[1] + oy * size))

def blitBush(bushData, biome, screen, ox = 0, oy = 0):
	global size, centerPos
	for i in bushData:
		screen.blit(biome[3], (centerPos[0] + size * i[0] + ox * size, centerPos[1] + size * i[1] + oy * size))

def blitBlock(blockData, biome, screen, ox = 0, oy = 0):
	global size, centerPos
	for i in blockData:
		screen.blit(biome[1], (centerPos[0] + size * i[0] + ox * size, centerPos[1] + size * i[1] + oy * size))

def blitBreakBlock(breakableData, biome, screen, ox = 0, oy = 0):
	global size, centerPos
	for i in breakableData:
		screen.blit(biome[2], (centerPos[0] + size * i[0] + ox * size, centerPos[1] + size * i[1] + oy * size))

def blitPlayer(playerxy, tp, screen, t, moving, mask):
	global size, centerPos

	tankType = tp[0]
	treadType = tp[1]

	tt = 0
	if moving: tt = int(t)

	g = size/2
	tank = Surface((size, size), SRCALPHA, 32)
	tank.blit(transform.rotate(treadType[tt % 2], playerxy[2] * 90), (0, 0))
	tank.blit(applyMask(tankType[playerxy[2]], mask, size), (0, 0))

	screen.blit(tank, (centerPos[0] + size * playerxy[0] - g, centerPos[1] + size * playerxy[1] - g))

def blitEnemies(enemies, screen, t, tankStats, tp):
	global size, centerPos, boss
	tanks, treads = tp[0], tp[1]
	g = size/2
	for i in enemies:
		tt = 0
		if i[4] > 0: tt = int(t)
		enemy = Surface((size, size), SRCALPHA, 32)
		enemy.blit(transform.rotate(treads[tankStats[i[3] + 1][4]][tt % 2], i[2] * 90), (0, 0))
		if i[-2] != 0: enemy.blit(boss[i[2]], (0, 0))
		else: enemy.blit(tanks[i[3]][i[2]], (0, 0))
		screen.blit(enemy, (centerPos[0] + size * i[0] - g, centerPos[1] + size * i[1] - g))

def blitBullets(bullets, screen):
	global bullet, size, centerPos
	g = size/2
	for i in bullets:
		if i[4] == 0: screen.blit(transform.rotate(enemyBullet, i[2]*90), (centerPos[0] + size * i[0] - g, centerPos[1] + size * i[1] - g))
		else: screen.blit(transform.rotate(bullet, i[2]*90), (centerPos[0] + size * i[0] - g, centerPos[1] + size * i[1] - g))

def blitPacks(healthPacks, ammoPacks, screen, heart, bullet):
	global centerPos, size

	for i in healthPacks:
		screen.blit(heart, (centerPos[0] + i[0] * size - size // 2, centerPos[1] + i[1] * size - size // 2))
	for i in ammoPacks:
		screen.blit(bullet, (centerPos[0] + i[0] * size - size // 2, centerPos[1] + i[1] * size - size // 2))

def blitSurround(screen, t, ox, oy, allData):
	data = allData[0]
	waterData = allData[1]
	bushData = allData[2]
	blockData = allData[3]
	breakableData = allData[4]
	biome = allData[6]

	blitRoom(data, screen, ox, oy)
	blitWater(waterData, screen, floor(t), ox, oy)
	blitBlock(blockData, biome, screen, ox, oy)
	blitBreakBlock(breakableData, biome, screen, ox, oy)
	blitBush(bushData, biome, screen, ox, oy)

def blitPet(petxy, playerxy, screen):
	global centerPos, size
	if playerxy[0] >= petxy[0]: c = "0"
	else: c = "1"
	screen.blit(eval(petxy[2] + c), (centerPos[0] + petxy[0] * size - size // 2, centerPos[1] + petxy[1] * size - size // 2))

def blitHealthBars(enemies, screen):
	global centerPos, size, healthBar
	for i in enemies:
		if i[-2] > 0:
			screen.blit(healthBar[int(13 * (i[8] / i[7]))], (centerPos[0] + (i[0] - 0.5) * size - size // 2, centerPos[1] + (i[1] - 0.5) * size - size // 2))

def blitGoldenUnlocks(rareLoot, screen):
	global centerPos, size, goldenUnlock
	for i in rareLoot:
		screen.blit(goldenUnlock, (centerPos[0] + i[0] * size - size * 0.25, centerPos[1] + i[1] * size - size * 0.25))