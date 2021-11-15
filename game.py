# Maxwell John Penders | pye3yh

import gamebox
import pygame
import random

### CONTANTS ###

CAMERAX = 800
CAMERAY = 600

# These two should be integers between 1 and 100 and divide evenly into the used dimensions of the map
MAXROOMSCALEX = 20
MAXROOMSCALEY = 20

ATTEMPTS = 200

### FUNCTIONS ###

# This generation function was inspired by https://journal.stuffwithstuff.com/2014/12/21/rooms-and-mazes/
# MUST BE ODD-SIZED DIMENSIONS
def generate_map(xdist, ydist):
	"""
	Takes in the x and y distances for the map to be generated and returns a generated map
	"""
	map = []

	# Generate empty x-by-y map filled with zeros
	for y in range(ydist):
		map.append([])
		for x in range(xdist):
			map[y].append(0)
	#print(map)
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
				if not (y_check<ydist and x_check<xdist):
					overlaps = True
				elif map[y_check][x_check] != 0:
					overlaps = True

		# If it doesn't conflict, change all squares to 1
		if not overlaps:
			for y_repl in range(y, y + room_y):
				for x_repl in range(x, x + room_x):
					map[y_repl][x_repl] = 1


	return map




### MAIN CODE BEGINS ###

for line in generate_map(100, 100):
	print(line)


camera = gamebox.Camera(CAMERAX, CAMERAY)
camera.y = 0






