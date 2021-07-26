import math, os

tiles = os.listdir("map")

def generateMap():
	mapList = [] #note: x and y is kinda inverted
	mapList.append([])
	for i in range(0, 15):
		mapList[0].append(["sea"])
	for i in range(1, 15):
		mapList.append([])
		for j in range(0, 15):
			if j == 0 or j == 14: mapList[i].append(["sea"])
			else: mapList[i].append(["forest"])
	mapList.append([])
	for i in range(0, 15):
		mapList[15].append(["sea"])
	print(mapList)
	mapList[4][4].append("1103")
	xyp = [4, 4]
	ut = []
	for i in range(0, 15):
		for h in tiles:
			a = ""
			a = a + str(mapList[xyp[1]][xyp[0]][1][0])
			a = a + str(mapList[xyp[1]][xyp[0]][1][1])
			print(int(a))
			if int(a) % 2 != 0:
				print("y")
	return mapList
generateMap()
"""
connectable up += 1
connectable right += 2
connectable down += 4
connectable left += 8
"""