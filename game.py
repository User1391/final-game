# Maxwell John Penders | pye3yh

import gamebox
import pygame
import random

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

### CLASSES ###

class grid_square:
	def __init__(self, i:int = 0, enemies:list = [], items:list = [], type:str = "none", visible:bool = False):
		self.value = i
		self.enemies = enemies
		self.items = items
		self.type = type
		self.visible = visible

class enemy:
	def __init__(self, health:int = 100,visible:bool = False):
		self.health = health
		self.visible = visible

### FUNCTIONS ###

def has_up(val):
	return (val >> 3) & 1 == 1

def has_down(val):
	return (val >> 2) & 1 == 1

def has_left(val):
	return (val >> 1) & 1 == 1

def has_right(val):
	return val & 1 == 1

#def divide(grid, mx, my, ax, ay):

# This generation function was an implementation of https://journal.stuffwithstuff.com/2014/12/21/rooms-and-mazes/
# MUST BE ODD-SIZED DIMENSIONS LARGER THAN 100 x 100
def generate_map(xdist, ydist):
	'''
	Takes in the x and y distances for the map to be generated and returns a generated map
	'''
	map = []

	# Generate empty x-by-y map filled with null squares
	for y in range(ydist):
		map.append([])
		for x in range(xdist):
			map[y].append(grid_square(-1,type="room"))

	# Go through and attempt to add a randomly sized room at each point, deleting it if it doesn't fit
	for attempt_num in range(ATTEMPTS):
		x = random.randint(1, xdist-1)
		y = random.randint(1, ydist-1)
		room_x = random.randint(2,xdist//MAXROOMSCALEX)
		room_y = random.randint(2,ydist//MAXROOMSCALEY)
		
		# Test if this room conflicts
		overlaps = False
		for y_check in range(y - 1, y + room_y + 1):
			for x_check in range(x - 1, x + room_x + 1):
				if not (y_check < ydist and x_check < xdist):
					overlaps = True
				elif map[y_check][x_check].value == 0b0000:
					overlaps = True

		# If it doesn't conflict, figure out how to layout the rooms and do it
		if not overlaps:
			for y_repl in range(y, y + room_y):
				for x_repl in range(x, x + room_x):

					val = 0b0000
					# If it's at a specific place on the rectangle, define it
					if y_repl == y:
						val |= 0b1000
					if y_repl == y + room_y - 1:
						val |= 0b0100
					if x_repl == x:
						val |= 0b0010
					if x_repl == x + room_x - 1:
						val |= 0b0001

					map[y_repl][x_repl].value = val

	# Next, we will fill out the edges with full walls, so that there is no going through the sides
	for yval in range(len(map)):
		map[yval][0].value = 0b1111
		map[yval][len(map[0]) - 1].value = 0b1111
	for xval in range(len(map[0])):
		map[0][xval].value = 0b1111
		map[len(map) - 1][xval].value = 0b1111

	# We now run a flood fill to generate our maze pattern
	
	starty, startx = 0, 0



	return map

### GAMEBOX VARIABLES ###

camera = gamebox.Camera(CAMERAX, CAMERAY)
camera.y = 0
projectiles = []
enemies = []

### MAIN CODE BEGINS ###

for line in generate_map(MAPX, MAPY):
	for value in line:
		print(value.value, end=' ')
	print()








