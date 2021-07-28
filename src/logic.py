from random import *
from math import *

def checkPlayerCollisions(playerxy, distanceToMove, wholeRoomData):
	if playerxy[2] == 0:
		if int(playerxy[1] - distanceToMove - 0.455 + 1) < 0.2: return playerxy
		k = int(wholeRoomData[int(playerxy[1] - distanceToMove - 0.455)][int(playerxy[0] + 0.455)])
		g = int(wholeRoomData[int(playerxy[1] - distanceToMove - 0.455)][int(playerxy[0] - 0.455)])
		if k == 1 or k == 4:
			if g == 1 or g == 4: playerxy[1] -= distanceToMove
	elif playerxy[2] == 2:
		if int(playerxy[1] + distanceToMove + 0.455) > 15.8: return playerxy
		k = int(wholeRoomData[int(playerxy[1] + distanceToMove + 0.455)][int(playerxy[0] + 0.45)])
		g = int(wholeRoomData[int(playerxy[1] + distanceToMove + 0.455)][int(playerxy[0] - 0.455)])
		if k == 1 or k == 4:
			if g == 1 or g == 4: playerxy[1] += distanceToMove
	elif playerxy[2] == 1:
		if int(playerxy[0] - distanceToMove - 0.455 + 1) < 0.2: return playerxy
		k = int(wholeRoomData[int(playerxy[1] + 0.455)][int(playerxy[0] - distanceToMove - 0.455)])
		g = int(wholeRoomData[int(playerxy[1] - 0.455)][int(playerxy[0] - distanceToMove - 0.455)])
		if k == 1 or k == 4:
			if g == 1 or g == 4: playerxy[0] -= distanceToMove
	elif playerxy[2] == 3:
		if int(playerxy[0] + distanceToMove + 0.455) > 19.8: return playerxy
		k = int(wholeRoomData[int(playerxy[1] + 0.455)][int(playerxy[0] + distanceToMove + 0.455)])
		g = int(wholeRoomData[int(playerxy[1] - 0.455)][int(playerxy[0] + distanceToMove + 0.455)])
		if k == 1 or k == 4:
			if g == 1 or g == 4: playerxy[0] += distanceToMove
	return playerxy

#have fun bleaching your eyes after seeing this ^^


#i did

def moveBullets(bullets):
	for i in range(0, len(bullets)):
		direction, bulletDistanceToMove = bullets[i][2], bullets[i][3]
		if direction == 0: bullets[i][1] -= bulletDistanceToMove
		elif direction == 1: bullets[i][0] -= bulletDistanceToMove
		elif direction == 2: bullets[i][1] += bulletDistanceToMove
		elif direction == 3: bullets[i][0] += bulletDistanceToMove
	return bullets

def spawnBullet(bullets, x, y, direction, bulletSpeed, fps):
	if direction == 0: bullets.append([x, y - 0.51, direction, bulletSpeed/fps])
	elif direction == 1: bullets.append([x - 0.51, y, direction, bulletSpeed/fps])
	elif direction == 2: bullets.append([x, y + 0.51, direction, bulletSpeed/fps])
	elif direction == 3: bullets.append([x + 0.51, y, direction, bulletSpeed/fps])
	return bullets

def checkBulletCollisions(bullets, wholeRoomData, breakableData):
	bullets2 = []
	for i in range(0, len(bullets)):
		x, y = int(bullets[i][0]), int(bullets[i][1])
		if bullets[i][0] < 0.2 or bullets[i][0] > 19.8 or bullets[i][1] < 0.2 or bullets[i][1] > 15.8: continue
		k = int(wholeRoomData[y][x])
		
		if k == 3:
			wholeRoomData[y][x] = 1
			breakableData.pop(breakableData.index([x, y]))
			continue
		elif k == 2: continue
		bullets2.append(bullets[i])
	return bullets2, wholeRoomData, breakableData

def spawnEnemy(enemies, x, y, tt):
	enemies.append([x, y, 1, tt, 0, 0, 0])

def spreadEnemy(enemies, wholeRoomData, tt):
	usableTiles = []
	for i in range(0, len(wholeRoomData)):
		for j in range(0, len(wholeRoomData[i])):
			if wholeRoomData[i][j] == "1" or wholeRoomData[i][j] == "4":
				usableTiles.append([i, j])
	while 1:
		a = 0
		g = randint(0, len(usableTiles)-1)
		for i in enemies:
			if i[0] == usableTiles[g][0] and i[1] == usableTiles[g][1]:
				a = 1
				break
		if not a:
			usedTile = usableTiles[g]
			break
	spawnEnemy(enemies, usedTile[1] + 0.5, usedTile[0] + 0.5, tt)

def roundTo8(x, base = 8):
	return int(base * math.ceil(float(x) / base) - 8)

def shootEnemies(enemies, bullets, wholeRoomData, tt, fps, playerxy):
	h = []
	for i in range(0, 20):
		h.append(0)
	for i in wholeRoomData:
		if len(i) > 0:
			for j in range(0, 19):
				if i[j] == "3":
					h[j] = 1

	for i in range(0, len(enemies)):
		enemies[i][5] += 1

		if int(playerxy[1]) == int(enemies[i][1]):
			if enemies[i][2] != 3:
				if int(playerxy[0]) > int(enemies[i][0]):
					enemies[i][2] = 3
			if enemies[i][2] != 1:
				if int(playerxy[0]) < int(enemies[i][0]):
					enemies[i][2] = 1
			if enemies[i][5] > tt[enemies[i][3] + 1][2]*fps/2 and randint(0, 30) == 0:
				enemies[i][5] = 0
				spawnBullet(bullets, enemies[i][0], enemies[i][1], enemies[i][2], tt[enemies[i][3] + 1][1], fps)

		elif "3" in wholeRoomData[int(enemies[i][1])]:
			if enemies[i][5] > tt[enemies[i][3] + 1][2]*fps/2 and randint(0, 30) == 0:
				enemies[i][5] = 0
				spawnBullet(bullets, enemies[i][0], enemies[i][1], enemies[i][2], tt[enemies[i][3] + 1][1], fps)
		if int(playerxy[0]) == int(enemies[i][0]):
			if enemies[i][2] != 2:
				if int(playerxy[1]) > int(enemies[i][1]):
					enemies[i][2] = 2
			if enemies[i][2] != 0:
				if int(playerxy[1]) < int(enemies[i][1]):
					enemies[i][2] = 0
			if enemies[i][5] > tt[enemies[i][3] + 1][2]*fps/2 and randint(0, 30) == 0:
				enemies[i][5] = 0
				spawnBullet(bullets, enemies[i][0], enemies[i][1], enemies[i][2], tt[enemies[i][3] + 1][1], fps)

		elif h[int(enemies[i][0])]:
			if enemies[i][5] > tt[enemies[i][3] + 1][2]*fps/2 and randint(0, 30) == 0:
				enemies[i][5] = 0
				spawnBullet(bullets, enemies[i][0], enemies[i][1], enemies[i][2], tt[enemies[i][3] + 1][1], fps)
	return enemies, bullets