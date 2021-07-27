from random import *

def checkPlayerCollisions(playerxy, distanceToMove, wholeRoomData):
	print(distanceToMove)
	if playerxy[2] == 0:
		k = int(wholeRoomData[int(playerxy[1] - distanceToMove - 0.48)][int(playerxy[0] + 0.48)])
		g = int(wholeRoomData[int(playerxy[1] - distanceToMove - 0.48)][int(playerxy[0] - 0.48)])
		if k == 1 or k == 4:
			if g == 1 or g == 4: playerxy[1] -= distanceToMove
	elif playerxy[2] == 2:
		k = int(wholeRoomData[int(playerxy[1] + distanceToMove + 0.48)][int(playerxy[0] + 0.48)])
		g = int(wholeRoomData[int(playerxy[1] + distanceToMove + 0.48)][int(playerxy[0] - 0.48)])
		if k == 1 or k == 4:
			if g == 1 or g == 4: playerxy[1] += distanceToMove
	elif playerxy[2] == 1:
		k = int(wholeRoomData[int(playerxy[1] + 0.48)][int(playerxy[0] - distanceToMove - 0.48)])
		g = int(wholeRoomData[int(playerxy[1] - 0.48)][int(playerxy[0] - distanceToMove - 0.48)])
		if k == 1 or k == 4:
			if g == 1 or g == 4: playerxy[0] -= distanceToMove
	elif playerxy[2] == 3:
		k = int(wholeRoomData[int(playerxy[1] + 0.48)][int(playerxy[0] + distanceToMove + 0.48)])
		g = int(wholeRoomData[int(playerxy[1] - 0.48)][int(playerxy[0] + distanceToMove + 0.48)])
		if k == 1 or k == 4:
			if g == 1 or g == 4: playerxy[0] += distanceToMove
	return playerxy

#have fun bleaching your eyes after seeing this ^^


#i did