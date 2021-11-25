# Maxwell John Penders | pye3yh

import gamebox
import pygame
import random
import math

# The map values mean the following:
# 0 - empty
# 1 - wall
# up down left right
# 69 will be a full block

### CONTANTS ###

MAPX = 100
MAPY = 100

CAMERAX = 800
CAMERAY = 600

# These two should be integers between 1 and 100 and divide evenly into the used dimensions of the map
MAXROOMSCALEX = 10
MAXROOMSCALEY = 10

# Best between 200 and 1100
ATTEMPTS = 600

# Distance rooms must be from each other
ROOM_DIST_Y = 3
ROOM_DIST_X = 3

SIZE = 100

MIN_CONN_DISTANCE = 20

### CLASSES ###


class enemy:
	def __init__(self, health: int = 100, visible: bool = False):
		self.health = health
		self.visible = visible

### FUNCTIONS ###

# This generation function was an implementation of https://journal.stuffwithstuff.com/2014/12/21/rooms-and-mazes/
# MUST BE ODD-SIZED DIMENSIONS LARGER THAN 100 x 100


def generate_rooms(xdist, ydist):
	'''
	Takes in the x and y distances for the map to be generated and returns a generated map and room list
	'''
	map = []
	rooms = []
	room_points = []

	# Generate empty x-by-y map filled with null squares
	for y in range(ydist):
		map.append([])
		for x in range(xdist):
			map[y].append(1)

	# Go through and attempt to add a randomly sized room at each point, deleting it if it doesn't fit
	for attempt_num in range(ATTEMPTS):
		x = random.randint(1, xdist-1)
		y = random.randint(1, ydist-1)
		room_x = random.randint(2, xdist//MAXROOMSCALEX)
		room_y = random.randint(2, ydist//MAXROOMSCALEY)

		# Test if this room conflicts
		overlaps = False
		for y_check in range(y - ROOM_DIST_Y, y + room_y + ROOM_DIST_Y):
			for x_check in range(x - ROOM_DIST_X, x + room_x + ROOM_DIST_X):
				if not (y_check < ydist and x_check < xdist):
					overlaps = True
				elif map[y_check][x_check] == 0:
					overlaps = True

		# If it doesn't conflict, figure out how to layout the rooms and do it
		if not overlaps:
			# Appends in tuple (top left x-cord, top left y-cord, x length, y length)
			rooms.append((x, y, room_x, room_y))
			for y_repl in range(y, y + room_y):
				for x_repl in range(x, x + room_x):
					map[y_repl][x_repl] = 0

	starty, startx = 0, 0

	return map, rooms


def generate_path(start_coords, end_coords):
	'''
 	Function that draws a path between two points
	'''
	
	total_x = end_coords[0] - start_coords[0]
	total_y = end_coords[1] - start_coords[1]
	node = start_coords
	to_draw = [start_coords]
	while node != end_coords:
		dx = end_coords[0] - node[0]
		dy = end_coords[1] - node[1]
		x_ratio = dx / total_x
		y_ratio = dy / total_y
		if x_ratio >= y_ratio:
			globals()["map"][node[1]][node[0] - 1 + 2 * (total_x > 0)] = 0
			node = (node[0] - 1 + 2 * (total_x > 0),node[1])
		else:
			globals()["map"][node[1] - 1 + 2 * (total_y > 0)][node[0]] = 0
			node = (node[0],node[1] - 1 + 2 * (total_y > 0))
		

lst = []

def generate_pathways(idx=1):
	'''
	Recursive function that outputs a map with single pathways drawn between rooms
	'''
	num_rooms = len(globals()["rooms"])
	if len(globals()["lst"]) == 0:
		globals()["lst"] = num_rooms * [0]
	idx_offset, rand2 = random.randint(1, 10), random.randint(0, max(idx - 1, 0))
	newidx = min(num_rooms - 1, idx + idx_offset)
	if (globals()["lst"][newidx] == 0):
		globals()["lst"][newidx] = 1
		start_coords = (globals()["rooms"][newidx][0] + random.randint(0, globals()["rooms"][newidx][2]), globals()["rooms"][newidx][1] + random.randint(0, globals()["rooms"][newidx][3]))
		end_coords = (globals()["rooms"][idx][0] + random.randint(0, globals()["rooms"][idx][2]), globals()["rooms"][idx][1] + random.randint(0, globals()["rooms"][idx][3]))
		if (dist_tuples(start_coords, end_coords) >= MIN_CONN_DISTANCE):
			generate_path(start_coords, end_coords)
		if(newidx != num_rooms):
			generate_pathways(newidx)
	# if (globals()["lst"][rand2] == 0):
	# 	#print(f"{idx} connected to {rand2}")
	# 	globals()["lst"][rand2] = 1
	# 	generate_pathways(rand2)

	return map, rooms

def dist_tuples(tuple1, tuple2):
	'''
	Finds distance between two (x,y) tuples
	'''
	return math.sqrt(math.pow(tuple2[0] - tuple1[0], 2) + math.pow(tuple2[1] - tuple1[1], 2)) 

### GAMEBOX VARIABLES ###

camera = gamebox.Camera(CAMERAX, CAMERAY)
camera.y = 0
projectiles = []
enemies = []

### MAIN CODE BEGINS ###

map, rooms = generate_rooms(MAPX, MAPY)
generate_pathways()
for longboi in map:
	for rum in longboi:
		print(rum,end='')
	print("")




