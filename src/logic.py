from random import *
from math import *

def checkPlayerCollisions(playerxy, distanceToMove, wholeRoomData, enemies):
	enemies2 = []
	for i in range(0, len(enemies)):
		enemies2.append([int(enemies[i][0] - 0.5), int(enemies[i][1] - 0.5)])
	if playerxy[2] == 0:
		if int(playerxy[1] - distanceToMove - 0.455 + 1) < 0.2: return playerxy
		y = int(playerxy[1] - distanceToMove - 0.455)
		k = int(wholeRoomData[y][int(playerxy[0] + 0.455)])
		g = int(wholeRoomData[y][int(playerxy[0] - 0.455)])
		if [int(playerxy[0] + 0.455), y] not in enemies2 and [y, int(playerxy[0] - 0.455)] not in enemies2 and (k == 1 or k == 4):
			if g == 1 or g == 4: playerxy[1] -= distanceToMove
	elif playerxy[2] == 2:
		if int(playerxy[1] + distanceToMove + 0.455) > 15.8: return playerxy
		y = int(playerxy[1] + distanceToMove + 0.455)
		k = int(wholeRoomData[y][int(playerxy[0] + 0.455)])
		g = int(wholeRoomData[y][int(playerxy[0] - 0.455)])
		if [int(playerxy[0] - 455), y] not in enemies2 and [int(playerxy[0] + 0.455), y] not in enemies2 and (k == 1 or k == 4):
			if g == 1 or g == 4: playerxy[1] += distanceToMove
	elif playerxy[2] == 1:
		if int(playerxy[0] - distanceToMove - 0.455 + 1) < 0.2: return playerxy
		x = int(playerxy[0] - distanceToMove - 0.455)
		k = int(wholeRoomData[int(playerxy[1] + 0.455)][x])
		g = int(wholeRoomData[int(playerxy[1] - 0.455)][x])
		if [x, int(playerxy[1] + 0.455)] not in enemies2 and [x, int(playerxy[1] - 0.455)] not in enemies2 and (k == 1 or k == 4):
			if g == 1 or g == 4: playerxy[0] -= distanceToMove
	elif playerxy[2] == 3:
		if int(playerxy[0] + distanceToMove + 0.455) > 19.8: return playerxy
		x = int(playerxy[0] + distanceToMove + 0.455)
		k = int(wholeRoomData[int(playerxy[1] + 0.455)][x])
		g = int(wholeRoomData[int(playerxy[1] - 0.455)][x])
		if [x, int(playerxy[1] + 0.455)] not in enemies2 and [x, int(playerxy[1] - 0.455)] not in enemies2 and (k == 1 or k == 4):
			if g == 1 or g == 4: playerxy[0] += distanceToMove
	return playerxy

def moveBullets(bullets):
	for i in range(0, len(bullets)):
		direction, bulletDistanceToMove = bullets[i][2], bullets[i][3]
		if direction == 0: bullets[i][1] -= bulletDistanceToMove
		elif direction == 1: bullets[i][0] -= bulletDistanceToMove
		elif direction == 2: bullets[i][1] += bulletDistanceToMove
		elif direction == 3: bullets[i][0] += bulletDistanceToMove
	return bullets

def spawnBullet(bullets, x, y, direction, bulletSpeed, fps, eop):
	if direction == 0: bullets.append([x, y - 0.51, direction, bulletSpeed/fps, eop])
	elif direction == 1: bullets.append([x - 0.51, y, direction, bulletSpeed/fps, eop])
	elif direction == 2: bullets.append([x, y + 0.51, direction, bulletSpeed/fps, eop])
	elif direction == 3: bullets.append([x + 0.51, y, direction, bulletSpeed/fps, eop])
	return bullets

def checkBulletCollisions(bullets, wholeRoomData, breakableData, playerxy, enemies, health, healthPacks, ammoPacks):
	bullets2, bullets3 = [], []
	for i in range(0, len(bullets)):
		x, y = int(bullets[i][0]), int(bullets[i][1])
		if bullets[i][0] < 0.2 or bullets[i][0] > 19.8 or bullets[i][1] < 0.2 or bullets[i][1] > 15.8: continue
		k = int(wholeRoomData[y][x])
		
		if bullets[i][4] == 0:
			for j in range(0, len(enemies)):
				if int(enemies[j][0]) == x and int(enemies[j][1]) == y:
					enemies.pop(j)
					k = 2
					if randint(0, 9) == 0:
						healthPacks.append([x + 0.5 + uniform(-0.2, 0.2), y + 0.5 + uniform(-0.2, 0.2)])
					else:
						for v in range(0, randint(0, 20)):
							ammoPacks.append([x + 0.5 + uniform(-0.2, 0.2), y + 0.5 + uniform(-0.2, 0.2)])
					break
		elif bullets[i][4] == 1:
			if int(playerxy[0]) == x and int(playerxy[1]) == y:
				health -= 1
				k = 2
				break

		if k == 3:
			wholeRoomData[y][x] = 1
			breakableData.pop(breakableData.index([x, y]))
			continue
		elif k == 2: continue
		bullets2.append(bullets[i])
		bullets3.append(bullets[i])
	for i in range(0, len(bullets2)):
		for j in range(0, len(bullets2)):
			if i == j: continue
			if int(bullets2[i][1]) == int(bullets2[j][1]) and int(bullets2[i][0]) == int(bullets2[j][0]) and bullets2[i] in bullets3 and bullets2[j] in bullets3:
				bullets3.pop(bullets3.index(bullets2[i]))
				bullets3.pop(bullets3.index(bullets2[j]))
	return bullets3, wholeRoomData, breakableData, enemies, health, healthPacks, ammoPacks

def spawnEnemy(enemies, x, y, tt):
	enemies.append([x, y, 1, tt, 0, 0, 0])

def spreadEnemy(enemies, wholeRoomData, tt, playerxy):
	usableTiles = []
	for i in range(0, len(wholeRoomData)):
		for j in range(0, len(wholeRoomData[i])):
			if wholeRoomData[i][j] == "1" or wholeRoomData[i][j] == "4":
				usableTiles.append([i, j])
	ticksi = 0
	while 1:
		if ticksi < 360: ticksi += 1
		else: break
		a = 0
		g = randint(0, len(usableTiles)-1)
		for i in enemies:
			if i[0] == usableTiles[g][0] and i[1] == usableTiles[g][1] or playerxy[0] == usableTiles[g][0] and playerxy[1] == usableTiles[g][1]:
				a = 1
				break
		if not a:
			usedTile = usableTiles[g]
			break
	if ticksi < 360: spawnEnemy(enemies, usedTile[1] + 0.5, usedTile[0] + 0.5, tt)

def roundTo8(x, base = 8):
	return int(base * math.ceil(float(x) / base) - 8)

def shootEnemies(enemies, bullets, wholeRoomData, tt, fps, playerxy):
	h = []
	for i in range(0, 21):
		h.append(0)
	for i in wholeRoomData:
		if len(i) > 0:
			for j in range(0, 19):
				if i[j] == "3":
					h[j] = 1

	for i in range(0, len(enemies)):
		enemies[i][5] += 1
		g = enemies[i][2]
		j = False
		if int(playerxy[1]) == int(enemies[i][1]):
			j = True
			if enemies[i][6] == 0 and enemies[i][4] == 0:
				if enemies[i][2] != 3:
					if int(playerxy[0]) > int(enemies[i][0]):
						enemies[i][2] = 3
				if enemies[i][2] != 1:
					if int(playerxy[0]) < int(enemies[i][0]):
						enemies[i][2] = 1
			if enemies[i][5] > tt[enemies[i][3] + 1][2]*fps/2 and randint(0, 30) == 0:
				enemies[i][5] = 0
				spawnBullet(bullets, enemies[i][0], enemies[i][1], enemies[i][2], tt[enemies[i][3] + 1][1], fps, 1)

		elif "3" in wholeRoomData[int(enemies[i][1])]:
			if enemies[i][5] > tt[enemies[i][3] + 1][2]*fps/2 and randint(0, 90) == 0:
				enemies[i][5] = 0
				spawnBullet(bullets, enemies[i][0], enemies[i][1], enemies[i][2], tt[enemies[i][3] + 1][1], fps, 1)
		
		if int(playerxy[0]) == int(enemies[i][0]):
			j = True
			if enemies[i][6] == 0 and enemies[i][4] == 0:
				if enemies[i][2] != 2:
					if int(playerxy[1]) > int(enemies[i][1]):
						enemies[i][2] = 2
				if enemies[i][2] != 0:
					if int(playerxy[1]) < int(enemies[i][1]):
						enemies[i][2] = 0
			if enemies[i][5] > tt[enemies[i][3] + 1][2]*fps/2 and randint(0, 30) == 0:
				enemies[i][5] = 0
				spawnBullet(bullets, enemies[i][0], enemies[i][1], enemies[i][2], tt[enemies[i][3] + 1][1], fps, 1)

		elif h[int(enemies[i][0])]:
			if enemies[i][5] > tt[enemies[i][3] + 1][2]*fps/2 and randint(0, 90) == 0:
				enemies[i][5] = 0
				spawnBullet(bullets, enemies[i][0], enemies[i][1], enemies[i][2], tt[enemies[i][3] + 1][1], fps, 1)
		if j == False and g == enemies[i][2] and enemies[i][4] == 0 and enemies[i][6] == 0 and randint(0, 120) == 0: enemies[i][2] = randint(0, 3)
	return enemies, bullets

def moveEnemies(enemies, wholeRoomData, fps, tankStats, playerxy):
	for i in range(0, len(enemies)):
		enemies2 = []
		for z in range(0, len(enemies)):
			if z != i: enemies2.append([int(enemies[z][0]), int(enemies[z][1])])
		x, y = enemies[i][0] - 0.5, enemies[i][1] - 0.5
		if enemies[i][6] > 0:
			if enemies[i][2] == 0:
				if y - enemies[i][4] < 0: pass
				elif int(playerxy[0]) == int(x) and int(playerxy[1]) == int(y - enemies[i][4]): pass
				elif wholeRoomData[int(y - enemies[i][4])][int(x)] == "4" or wholeRoomData[int(y - enemies[i][4])][int(x)] == "1":
					enemies[i][1] -= enemies[i][4]
					enemies[i][6] -= 1
					continue
				
			elif enemies[i][2] == 3:
				if x + enemies[i][4] > 19: pass
				elif int(playerxy[0]) == int(x + enemies[i][4]) and int(playerxy[1]) == int(y): pass
				elif wholeRoomData[int(y)][int(x + enemies[i][4])] == "4" or wholeRoomData[int(y)][int(x + enemies[i][4])] == "1":
					enemies[i][0] += enemies[i][4]
					enemies[i][6] -= 1
					continue
				
			elif enemies[i][2] == 2:
				if y + enemies[i][4] > 15: pass
				elif int(playerxy[0]) == int(x) and int(playerxy[1]) == int(y + enemies[i][4]): pass
				elif wholeRoomData[int(y + enemies[i][4])][int(x)] == "4" or wholeRoomData[int(y + enemies[i][4])][int(x)] == "1":
					enemies[i][1] += enemies[i][4]
					enemies[i][6] -= 1
					continue
				
			elif enemies[i][2] == 1:
				if x - enemies[i][4] < 0: pass 
				elif int(playerxy[0]) == int(x - enemies[i][4]) and int(playerxy[1]) == int(y): pass
				elif wholeRoomData[int(y)][int(x - enemies[i][4])] == "4" or wholeRoomData[int(y)][int(x - enemies[i][4])] == "1":
					enemies[i][0] -= enemies[i][4]
					enemies[i][6] -= 1
					continue
			
			enemies[i][0] = int(enemies[i][0]) + 0.5
			enemies[i][1] = int(enemies[i][1]) + 0.5
			enemies[i][4], enemies[i][6] = 0, 0
		elif randint(0, 60) == 0:
			enemies[i][0] = int(enemies[i][0]) + 0.5
			enemies[i][1] = int(enemies[i][1]) + 0.5
			l = False
			if enemies[i][2] == 0:
				if y - 1 >= 0 and [x, y - 1] not in enemies2:
					if wholeRoomData[int(y - 1)][int(x)] == "4" or wholeRoomData[int(y - 1)][int(x)] == "1":
						l = True
			elif enemies[i][2] == 3:
				if x + 1 <= 19 and [x + 1, y] not in enemies2:
					if wholeRoomData[int(y)][int(x + 1)] == "4" or wholeRoomData[int(y)][int(x + 1)] == "1":
						l = True
			elif enemies[i][2] == 2:
				if y + 1 <= 15 and [x, y + 1] not in enemies2:
					if wholeRoomData[int(y + 1)][int(x)] == "4" or wholeRoomData[int(y + 1)] == "1":
						l = True
			elif enemies[i][2] == 1:
				if x - 1 >= 0 and [x - 1, y] not in enemies2:
					if wholeRoomData[int(y)][int(x - 1)] == "4" or wholeRoomData[int(y)][int(x - 1)] == "1":
						l = True
			if l:
				enemies[i][4] = tankStats[enemies[i][3]+1][0] / fps
				enemies[i][6] = int(1 / enemies[i][4])
		else: enemies[i][4], enemies[i][6], enemies[i][0], enemies[i][1] = 0, 0, int(enemies[i][0]) + 0.5, int(enemies[i][1]) + 0.5

def pickupPacks(health, ammo, healthPacks, ammoPacks, playerxy):
	healthPacks2, ammoPacks2 = [], []
	for i in range(0, len(healthPacks)):
		if int(healthPacks[i][0]) == int(playerxy[0]) and int(healthPacks[i][1]) == int(playerxy[1]):
			health += 1
			continue
		healthPacks2.append(healthPacks[i])
	for i in range(0, len(ammoPacks)):
		if int(ammoPacks[i][0]) == int(playerxy[0]) and int(ammoPacks[i][1]) == int(playerxy[1]):
			ammo += 1
			continue
		ammoPacks2.append(ammoPacks[i])
	return health, ammo, healthPacks2, ammoPacks2