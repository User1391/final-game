# Maxwell John Penders | pye3yh

''' 
Checkpoint 1
Overall game description:
My goal is to create a roguelike RPG in which the character has a ranged weapon. There will be no win state for the game, as it will go forever until the character dies.
The character will be able to pick up items and gain levels, which will increase the character's skills. Most importantly, each level will have a random generation,
so each playthrough is unique.

The Five Main Requirements:
User Input - The player will have movement control through the WASD keys and control over other actions through other keyboard keys.
Start Screen - There will be a start screen with game name, name and ID, and basic game instructions
Game Over - Once the player's health reaches 0, they will die and see the Game Over screen
Small Enough Window - The window size will be set to 800x600
Graphics - I will use appropriate sprite graphics and overall graphical themes

At Least 4 for Secondary Requirements:
Enemies - The player will have to fight against enemies to win
Scrolling Level - In order to access the full map, the map will scroll to follow the player
Health Bar - the player will have a health bar that will end the game once it reaches 0
Multiple Levels - the game will have infinite levels that can generate one after another
'''

import gamebox
import pygame
import random
import math
from enum import Enum
import sys

### CONTANTS ###
# Okay, so just to clarify, the first language I ever learned was Java, so I uppercase all my constants like all the cool kids

GAMENAME = "Frustration Factor"

PATHWAY_ROOM_RADIUS = 5

ENEMY_RANGE = 7

FRAME_SKIP = 10

PROJ_SPEED = 15

BLOCKSIZE = 50

CHARACTERSIZE = 30

MOVEMENT_SPEED = 10

MIN_ENDING_DIST = 30

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

# Please be okay with enum, it's so nice
class gameState(Enum):
	MENU = 1
	GEN_MAP = 2
	IN_GAME = 3
	CREATE_WALLS = 4
	RENDER = 5
	NEXT_LEVEL = 6
	DEAD = 7
	ADD_ENEMIES = 8

# Yeah, so I've done coding before this class. If it's really not okay to do this, tell me, but it'll be a pain to switch to lists
class Enemy:
	def __init__(self, health: int = 100, curr_square: tuple = (0,0), target_square: tuple = (0,0)):
		self.health = health
		self.curr_square = curr_square
		self.target_square = target_square

class Projectile:
	def __init__(self, damage: int = 20, curr_pos: tuple = (0,0), target_pos: tuple = (0,0)):
		self.damage = damage
		self.curr_pos = curr_pos
		self.target_pos = target_pos
		self.start_pos = curr_pos


### FUNCTIONS ###

# MUST BE ODD-SIZED DIMENSIONS LARGER THAN 100 x 100

def center_of_rect(rect_tuple):
	'''
	Takes in a rectangular tuple (top left x-cord, top left y-cord, x length, y length) and returns the approximate center pixel
	'''
	x_coord = rect_tuple[0] + rect_tuple[2]//2
	y_coord = rect_tuple[1] + rect_tuple[3]//2
	return (x_coord, y_coord)


def random_pos_tuple(rect_tuple):
	'''
	Takes in a rectangular tuple (top left x-cord, top left y-cord, x length, y length) and outputs a random position within
	'''
	return (rect_tuple[0] + random.randint(0, rect_tuple[2] - 1), rect_tuple[1] + random.randint(0, rect_tuple[3] - 1))

# I got this great idea from https://journal.stuffwithstuff.com/2014/12/21/rooms-and-mazes/
# I wrote all of this code myself, though, without looking at any sort of code for it
def generate_rooms(xdist, ydist):
	'''
	Takes in the x and y distances for the map to be generated and returns a generated map and room list
	'''
	fin_map = []
	rooms = []
	room_points = []

	# Generate empty x-by-y map filled with null squares
	for y in range(ydist):
		fin_map.append([])
		for x in range(xdist):
			fin_map[y].append(1)

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
				elif fin_map[y_check][x_check] == 0:
					overlaps = True

		# If it doesn't conflict, figure out how to layout the rooms and do it
		if not overlaps:
			# Appends in tuple (top left x-cord, top left y-cord, x length, y length)
			rooms.append((x, y, room_x, room_y))
			for y_repl in range(y, y + room_y):
				for x_repl in range(x, x + room_x):
					fin_map[y_repl][x_repl] = 0

	starty, startx = 0, 0

	return fin_map, rooms


def generate_path(start_coords, end_coords):
	'''
 	Function that draws a path between two points
	'''
	total_x = end_coords[0] - start_coords[0]
	total_y = end_coords[1] - start_coords[1]
	if total_y * total_x == 0:
		return 
	node = start_coords
	to_draw = [start_coords]
	while node != end_coords:
		dx = end_coords[0] - node[0]
		dy = end_coords[1] - node[1]
		x_ratio = dx / total_x
		y_ratio = dy / total_y
		if x_ratio == 0.5 and y_ratio == 0.5:
			globals()["enemies"].append(Enemy(100, node, node))
		if x_ratio >= y_ratio:
			globals()["fin_map"][node[1]][node[0] - 1 + 2 * (total_x > 0)] = 0
			node = (node[0] - 1 + 2 * (total_x > 0),node[1])
		else:
			globals()["fin_map"][node[1] - 1 + 2 * (total_y > 0)][node[0]] = 0
			node = (node[0],node[1] - 1 + 2 * (total_y > 0))
		


lst = []
def generate_pathways():
	'''
	Function that outputs a map using a BFS algorithm
	'''
	num_rooms = len(globals()["rooms"])
	all_rooms = globals()["rooms"]
	visited_rooms = []
	queue = []
	last_room = all_rooms.pop()
	globals()["ending_room"] = last_room
	queue.append(last_room)
	while queue:
		queued_room = queue.pop(0)
		for ind_room in all_rooms:
			if ind_room not in visited_rooms and dist_tuples(center_of_rect(ind_room),center_of_rect(queued_room)) <= PATHWAY_ROOM_RADIUS * BLOCKSIZE:
				generate_path(center_of_rect(queued_room), center_of_rect(ind_room))
				globals()["lst"].append([queued_room, ind_room])
				globals()["connected_rooms"].append(ind_room)
				queue.append(ind_room)
				all_rooms.remove(ind_room)
				visited_rooms.append(ind_room)

	return fin_map, rooms

def dist_tuples(tuple1, tuple2):
	'''
	Finds distance between two (x,y) tuples
	'''
	return math.sqrt(math.pow(tuple2[0] - tuple1[0], 2) + math.pow(tuple2[1] - tuple1[1], 2)) 

### GAMEBOX VARIABLES ###
# Enjoy trying to read through this, my favorite TA! Definitely don't have excess variables!

camera = gamebox.Camera(CAMERAX, CAMERAY)
camera.y = 0
enemy_projectiles = []
human_projectiles = []
enemies = []
current_health = 100
# Right, so it's called fin_map because map is an actual thing in python
fin_map = []
walls = []
connected_rooms = []
score = 1
character = gamebox.from_color(0, 0, "blue",CHARACTERSIZE, CHARACTERSIZE)
endx = 0
endy = 0
end_square = gamebox.from_color(endx, endy, "yellow",BLOCKSIZE-1, BLOCKSIZE-1)
health_bar = gamebox.from_color(0, 0, "red", current_health * 2, 20)
count = 1
can_shoot = False
ending_room = []
human_count = 1
can_shoot_human = False

game_state = gameState.MENU

### MAIN CODE BEGINS ###

def tick(keys):
	global game_state, fin_map, MAPX, MAPY, walls, enemies, enemy_projectiles, human_projectiles,current_health, BLOCKSIZE, character, score, connected_rooms, lst, endx, endy, health_bar, count, can_shoot, ending_room, human_count, can_shoot_human

	camera.clear("white")

	if count % FRAME_SKIP == 0:
		can_shoot = True
	else:
		can_shoot = False

	if human_count > FRAME_SKIP:
		can_shoot_human = True
	else:
		can_shoot_human = False

	# Menu display
	if game_state == gameState.MENU:
		# Set camera to viewing center of start screen, just so that when we start everything is all good
		camera.y == CAMERAY//2
		camera.x == CAMERAX//2

		play_box_x = camera.x
		play_box_y = camera.y + CAMERAY//4
		play_box_x_size = 150
		play_box_y_size = 70

		name_text = gamebox.from_text(camera.x, camera.y - CAMERAY//4, GAMENAME, 50, "blue", bold=False, italic=False)
		creator_info_text = gamebox.from_text(camera.x, camera.y - CAMERAY//3, "Maxwell Penders - pye3yh", 30, "blue", bold=False, italic=False)
		instructions_text = gamebox.from_text(camera.x, camera.y, "Move using WASD. Fire with the spacebar. Don't die. Good luck!", 30, "blue", bold=False, italic=False)
		play_box = gamebox.from_color(play_box_x, play_box_y, "black", play_box_x_size, play_box_y_size)
		play_text = gamebox.from_text(play_box_x, play_box_y, "PLAY", 60, "red", bold=True, italic=False)

		camera.draw(name_text)
		camera.draw(creator_info_text)
		camera.draw(play_box)
		camera.draw(play_text)
		camera.draw(instructions_text)

		in_box=camera.mouseclick and (play_box_x-play_box_x_size//2)<=camera.mousex<=(play_box_x+play_box_x_size//2) and (play_box_y-play_box_y_size//2)<=camera.mousey<=(play_box_y+play_box_y_size//2)
		if in_box:
			game_state = gameState.GEN_MAP

	elif game_state == gameState.GEN_MAP:

		#TODO: Make a separate list of walls adjacent to emptiness

		connected_rooms = []
		globals()["fin_map"], globals()["rooms"] = generate_rooms(MAPX, MAPY)
		#print(globals()["rooms"])
		globals()["fin_map"], globals()["rooms"] = generate_pathways()
		# for line in globals()["fin_map"]:
		# 	for thing in line:
		# 		print(thing,end='')
		# 	print("")
		game_state = gameState.CREATE_WALLS

	elif game_state == gameState.CREATE_WALLS:
		# Time to wall out
		#print(len(globals()["fin_map"]))
		for y in range(len(globals()["fin_map"]) - 1):
			for x in range(len(globals()["fin_map"][0]) - 1):
				#print(y, x)
				if globals()["fin_map"][y][x] == 1:
					walls.append(gamebox.from_color(x * BLOCKSIZE, y * BLOCKSIZE, "black", BLOCKSIZE, BLOCKSIZE))
		
		game_state = gameState.ADD_ENEMIES
	elif game_state == gameState.ADD_ENEMIES:


		game_state = gameState.IN_GAME
		######## THIS SETS UP DA STUFF (great comment) ########
		
		
		#print(connected_rooms)
		# print(walls)

		starting_room = random.choice(connected_rooms)
		connected_rooms.remove(starting_room)

		character.y = random.randint(starting_room[1], starting_room[1] + starting_room[3] - 1) * BLOCKSIZE
		character.x = random.randint(starting_room[0], starting_room[0] + starting_room[2] - 1) * BLOCKSIZE
		end_coord_pos = random_pos_tuple(ending_room)
		end_square.x = end_coord_pos[0] * BLOCKSIZE
		end_square.y = end_coord_pos[1] * BLOCKSIZE
		#print(end_square.x/50,end_square.y/50)
		while dist_tuples((end_square.x, end_square.y), (character.x, character.y)) <= MIN_ENDING_DIST * BLOCKSIZE:
			starting_room = random.choice(connected_rooms)
			connected_rooms.remove(starting_room)
			character.y = random.randint(starting_room[1], starting_room[1] + starting_room[3] - 1) * BLOCKSIZE
			character.x = random.randint(starting_room[0], starting_room[0] + starting_room[2] - 1) * BLOCKSIZE
		camera.y = character.y 
		camera.x = character.x
		#print("Character", character.x/50, character.y/50)

		#print("End",end_square.x, end_square.y)
		######################################################

		# Adding enemies
		for square in connected_rooms:
			enemies.append(Enemy(100, random_pos_tuple(square), random_pos_tuple(square)))
			

	elif game_state == gameState.RENDER:

		# For dev testing
		if pygame.K_a in keys:
			camera.x -= 30
		if pygame.K_d in keys:
			camera.x += 30
		if pygame.K_s in keys:
			camera.y += 30
		if pygame.K_w in keys:
			camera.y -= 30

		for wall in walls:
			camera.draw(wall)

		

		camera.draw(character)
		camera.draw(end_square)


	elif game_state == gameState.IN_GAME:

		# Character movement
		if pygame.K_a in keys:
			character.x -= MOVEMENT_SPEED
		if pygame.K_d in keys:
			character.x += MOVEMENT_SPEED
		if pygame.K_s in keys:
			character.y += MOVEMENT_SPEED
		if pygame.K_w in keys:
			character.y -= MOVEMENT_SPEED

		# Character firing
		if can_shoot_human and pygame.K_SPACE in keys:
			#print(camera.mouse)
			human_count = 0
			#target_x = character.x + ((camera.mousex - character.x) * (dist_tuples((int(camera.mouse[0]/BLOCKSIZE),int(camera.mouse[1]/BLOCKSIZE)),(character.x / BLOCKSIZE, character.y / BLOCKSIZE)) * ENEMY_RANGE))
			#target_y = character.y + ((camera.mousey - character.y) * (dist_tuples((int(camera.mouse[0]/BLOCKSIZE),int(camera.mouse[1]/BLOCKSIZE)),(character.x / BLOCKSIZE, character.y / BLOCKSIZE)) * ENEMY_RANGE))
			human_projectiles.append(Projectile(50, (character.x, character.y), (camera.mousex, camera.mousey)))


		#TODO: Group walls together	for projectile optimization
		for wall in walls:
			if character.touches(wall):
				character.move_to_stop_overlapping(wall)
			if end_square.touches(wall):
				end_square.move_to_stop_overlapping(wall)
			
			camera.draw(wall)

		for enemy in enemies:
			
			if count % 20 == 0:
				rand_dir = random.randint(1,4)
				if rand_dir == 1 and fin_map[enemy.curr_square[1] + 1][enemy.curr_square[0]] == 0:
					enemy.curr_square = (enemy.curr_square[0], enemy.curr_square[1] + 1)
				if rand_dir == 2 and fin_map[enemy.curr_square[1] - 1][enemy.curr_square[0]] == 0:
					enemy.curr_square = (enemy.curr_square[0], enemy.curr_square[1] - 1)
				if rand_dir == 3 and fin_map[enemy.curr_square[1]][enemy.curr_square[0] + 1] == 0:
					enemy.curr_square = (enemy.curr_square[0] + 1, enemy.curr_square[1])
				if rand_dir == 4 and fin_map[enemy.curr_square[1]][enemy.curr_square[0] - 1] == 0:
					enemy.curr_square = (enemy.curr_square[0] - 1, enemy.curr_square[1])

			camera.draw(gamebox.from_color(enemy.curr_square[0] * BLOCKSIZE, enemy.curr_square[1] * BLOCKSIZE, "green", 20, 20))
			

			if dist_tuples(enemy.curr_square,(character.x / BLOCKSIZE, character.y / BLOCKSIZE)) <= ENEMY_RANGE and can_shoot:
				target_x = enemy.curr_square[0] * BLOCKSIZE + ((character.x - enemy.curr_square[0] * BLOCKSIZE) * (dist_tuples(enemy.curr_square,(character.x / BLOCKSIZE, character.y / BLOCKSIZE)) * ENEMY_RANGE))
				target_y = enemy.curr_square[1] * BLOCKSIZE + ((character.y - enemy.curr_square[1] * BLOCKSIZE) * (dist_tuples(enemy.curr_square,(character.x / BLOCKSIZE, character.y / BLOCKSIZE)) * ENEMY_RANGE))
				enemy_projectiles.append(Projectile(20, (enemy.curr_square[0] * BLOCKSIZE, enemy.curr_square[1] * BLOCKSIZE), (target_x, target_y)))

			if enemy.health <= 0:
				enemies.remove(enemy)
		
		to_remove_proj_hum = []
		for proj in human_projectiles:
			removed = False
			curr_x, curr_y = proj.curr_pos[0], proj.curr_pos[1] 
			tar_x, tar_y = proj.target_pos[0], proj.target_pos[1]
			start_x, start_y = proj.start_pos[0], proj.start_pos[1]

			final_x, final_y = 0, 0

			for enemy in enemies:
				if dist_tuples(proj.curr_pos,(enemy.curr_square[0] * BLOCKSIZE, enemy.curr_square[1] * BLOCKSIZE)) <= BLOCKSIZE // 2:
					enemy.health -= proj.damage
					to_remove_proj_hum.append(proj)

			total_dist = dist_tuples(proj.target_pos, proj.curr_pos)

			if total_dist >= PROJ_SPEED:
				dy = (tar_y - curr_y) / total_dist * PROJ_SPEED
				dx = (tar_x - curr_x) / total_dist * PROJ_SPEED

				final_x += round(dx)
				final_y += round(dy)

				proj.curr_pos = (curr_x + final_x, curr_y + final_y)
				camera.draw(gamebox.from_color(proj.curr_pos[0], proj.curr_pos[1], "orange", 5, 5))
			else:
				to_remove_proj_hum.append(proj)
				removed = True
		
			if not removed and fin_map[int(proj.curr_pos[1]//BLOCKSIZE)][int(proj.curr_pos[0]//BLOCKSIZE)] == 1:
				to_remove_proj_hum.append(proj)

		to_remove_proj_hum = list(dict.fromkeys(to_remove_proj_hum))
		for to_remove in to_remove_proj_hum:
			human_projectiles.remove(to_remove)

		to_remove_proj = []
		for proj in enemy_projectiles:
			removed = False

			curr_x, curr_y = proj.curr_pos[0], proj.curr_pos[1] 
			tar_x, tar_y = proj.target_pos[0], proj.target_pos[1]
			start_x, start_y = proj.start_pos[0], proj.start_pos[1]

			final_x, final_y = 0, 0
			
			if dist_tuples(proj.curr_pos,(character.x, character.y)) <= CHARACTERSIZE // 2:
				current_health -= proj.damage
				to_remove_proj.append(proj)

			total_dist = dist_tuples(proj.target_pos, proj.curr_pos)

			if total_dist >= PROJ_SPEED:
				dy = (tar_y - curr_y) / total_dist * PROJ_SPEED
				dx = (tar_x - curr_x) / total_dist * PROJ_SPEED

				final_x += round(dx)
				final_y += round(dy)

				proj.curr_pos = (curr_x + final_x, curr_y + final_y)
				camera.draw(gamebox.from_color(proj.curr_pos[0], proj.curr_pos[1], "purple", 5, 5))
			else:
				to_remove_proj.append(proj)
				removed = True
		
			if not removed and fin_map[int(proj.curr_pos[1]//BLOCKSIZE)][int(proj.curr_pos[0]//BLOCKSIZE)] == 1:
				to_remove_proj.append(proj)

		to_remove_proj = list(dict.fromkeys(to_remove_proj))
		for to_remove in to_remove_proj:
			enemy_projectiles.remove(to_remove)
			

		if character.touches(end_square):
			score += 1
			current_health = 100
			count = 1
			human_count = 1
			game_state = gameState.NEXT_LEVEL

		camera.y = character.y 
		camera.x = character.x
		#print(camera.x//50, camera.y//50)

		health_bar = gamebox.from_color(0, 0, "red", current_health * 2, 20)

		health_bar.y = camera.y - 250
		health_bar.x = camera.x - 250

		score_text = gamebox.from_text(camera.x + 350, camera.y + 250, str(score), 50, "red", bold=False, italic=False)

		# IDK this end square is on drugs or something
		# w

		if current_health <= 0:
			game_state = gameState.DEAD

		camera.draw(character)
		camera.draw(end_square)
		camera.draw(health_bar)
		camera.draw(score_text)

	elif game_state == gameState.NEXT_LEVEL:
		# Set camera to viewing center of start screen, just so that when we start everything is all good
		camera.y == CAMERAY//2
		camera.x == CAMERAX//2
		instructions_text = gamebox.from_text(camera.x, camera.y, "Press SPACE to continue", 50, "blue", bold=False, italic=False)
		if pygame.K_SPACE in keys:
			walls.clear()
			enemies.clear()
			enemy_projectiles.clear()
			fin_map.clear()
			connected_rooms.clear()
			lst.clear()

			game_state = gameState.GEN_MAP

		camera.draw(instructions_text)

	elif game_state == gameState.DEAD:
		# Set camera to viewing center of start screen, just so that when we start everything is all good
		camera.y == CAMERAY//2
		camera.x == CAMERAX//2
		instructions_text = gamebox.from_text(camera.x, camera.y, "You are dead. Press R to play again!", 50, "red", bold=False, italic=False)
		score_text = gamebox.from_text(camera.x, camera.y + 100, "Score: " + str(score), 50, "red", bold=False, italic=False)
		if pygame.K_r in keys:
			walls.clear()
			enemies.clear()
			enemy_projectiles.clear()
			fin_map.clear()
			connected_rooms.clear()
			lst.clear()
			score = 1
			current_health = 100
			count = 1
			human_count = 1

			game_state = gameState.GEN_MAP

		camera.draw(instructions_text)

	count += 1
	human_count += 1 
	camera.display()

gamebox.timer_loop(30, tick)
