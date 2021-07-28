from random import *

def checkPlayerCollisions(playerxy, distanceToMove, wholeRoomData):
	if playerxy[2] == 0:
		k = int(wholeRoomData[int(playerxy[1] - distanceToMove - 0.46)][int(playerxy[0] + 0.46)])
		g = int(wholeRoomData[int(playerxy[1] - distanceToMove - 0.46)][int(playerxy[0] - 0.46)])
		if k == 1 or k == 4:
			if g == 1 or g == 4: playerxy[1] -= distanceToMove
	elif playerxy[2] == 2:
		k = int(wholeRoomData[int(playerxy[1] + distanceToMove + 0.46)][int(playerxy[0] + 0.46)])
		g = int(wholeRoomData[int(playerxy[1] + distanceToMove + 0.46)][int(playerxy[0] - 0.46)])
		if k == 1 or k == 4:
			if g == 1 or g == 4: playerxy[1] += distanceToMove
	elif playerxy[2] == 1:
		k = int(wholeRoomData[int(playerxy[1] + 0.46)][int(playerxy[0] - distanceToMove - 0.46)])
		g = int(wholeRoomData[int(playerxy[1] - 0.46)][int(playerxy[0] - distanceToMove - 0.46)])
		if k == 1 or k == 4:
			if g == 1 or g == 4: playerxy[0] -= distanceToMove
	elif playerxy[2] == 3:
		k = int(wholeRoomData[int(playerxy[1] + 0.46)][int(playerxy[0] + distanceToMove + 0.46)])
		g = int(wholeRoomData[int(playerxy[1] - 0.46)][int(playerxy[0] + distanceToMove + 0.46)])
		if k == 1 or k == 4:
			if g == 1 or g == 4: playerxy[0] += distanceToMove
	return playerxy

#have fun bleaching your eyes after seeing this ^^


#i did

def moveBullets(bullets):
	for i in range(0, len(bullets)):
		direction, bulletDistanceToMove = bullets[i][2], bullets[i][3]
		if direction == 0: bullets[i][1] -= bulletDistanceToMove
		elif direction == 3: bullets[i][0] += bulletDistanceToMove
		elif direction == 2: bullets[i][1] += bulletDistanceToMove
		elif direction == 1: bullets[i][0] -= bulletDistanceToMove
	return bullets

def spawnBullet(bullets, x, y, direction, bulletSpeed, fps):
	if direction == 0: bullets.append([x, y - 0.51, direction, bulletSpeed/fps])
	elif direction == 3: bullets.append([x + 0.51, y, direction, bulletSpeed/fps])
	elif direction == 2: bullets.append([x, y + 0.51, direction, bulletSpeed/fps])
	elif direction == 1: bullets.append([x - 0.51, y, direction, bulletSpeed/fps])
	return bullets

def checkBulletCollisions(bullets, wholeRoomData, breakableData):
	bullets2 = []
	for i in range(0, len(bullets)):
		x, y = int(bullets[i][0]), int(bullets[i][1])
		if bullets[i][0] < 0.2 or bullets[i][0] > 19.8 or bullets[i][1] < 0.2 or bullets[i][1] > 19.8: continue
		k = int(wholeRoomData[y][x])
		
		if k == 3:
			wholeRoomData[y][x] = 1
			breakableData.pop(breakableData.index([x, y]))
			continue
		elif k == 2: continue
		bullets2.append(bullets[i])
	return bullets2, wholeRoomData, breakableData