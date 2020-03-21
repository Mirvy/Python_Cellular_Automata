import pygame, sys, random, math
from os import system, name
from typing import List, Callable

#Generic colors for testing
colors = {
	'black'  : (0, 0, 0),
	'white'  : (255, 255, 255),
	'red'    : (255, 57, 51),
	'green'  : (22, 238, 35),
	'blue'   : (8, 58, 242),
	'yellow' : (221, 242, 8)
}

#Generates a starting grid, using the callback function passed.
def generate_grid(size,callback):
	grid = [[0 for x in range(size)] for y in range(size)]
	grid = callback(grid)
	return grid

#Draws the grid to the screen
def render_grid(surface,grid,size=10):
	for i in range(len(grid)):
		for j in range(len(grid)):
			if grid[i][j] == 0:
				color = colors['black']
			else:
				color = colors['white']
		#Commented out this portion which produces a grid
		#	which is good for testing but makes the presentation
		#	hard to look at.
			# pygame.draw.rect(
				# surface,
				# colors['white'],
				# pygame.Rect(
					# (size*j),
					# (i*size),
					# size-(size//5),
					# size)
				# )
			pygame.draw.rect(
				surface,
				color,
				pygame.Rect(
				(size*j)+1,
				(i*size)+1,
				size-(size//5)-2,
				size-2)
			)

#Calculates immediate neighbor count; edges will wrap to
#	opposing sides.
def find_neighbors(grid,row,col):
	adjacent = []
	for dx in (-1,0,1):
		for dy in (-1,0,1):
			if dx != 0 or dy != 0:
				adjacent.append([(row+dy)%len(grid),(col+dx)%len(grid)])
	return adjacent

#Determines the next generation for a given cell based on
#	its current state, and its neighbor count.
def process_cell(cell_state,neighbor_count):
	if cell_state == 1 and (neighbor_count >= 4 or neighbor_count <= 1):
		return 0
	if cell_state == 0 and neighbor_count == 3:
		return 1
	return cell_state
	
#Format helper function for clearing the console.
def clear():
	if name == 'nt':
	#for windows
		_ = system('cls')
	#for mac and linux
	else:
		_ = system('clear')
	
#Pattern Initialization Callbacks for generating
#	different initial states for the grid.
#--Static(nonchanging)--
def pattern_block(grid):
	grid[GRID_LENGTH//2][GRID_LENGTH//2]         = 1
	grid[GRID_LENGTH//2][(GRID_LENGTH//2)+1]     = 1
	grid[(GRID_LENGTH//2)+1][GRID_LENGTH//2]     = 1
	grid[(GRID_LENGTH//2)+1][(GRID_LENGTH//2)+1] = 1
	return grid
	
def pattern_loaf(grid):
	grid[(GRID_LENGTH//2)-1][GRID_LENGTH//2]     = 1
	grid[(GRID_LENGTH//2)-1][(GRID_LENGTH//2)-1] = 1
	grid[GRID_LENGTH//2][(GRID_LENGTH//2)-2]     = 1
	grid[GRID_LENGTH//2][(GRID_LENGTH//2)+1]     = 1
	grid[(GRID_LENGTH//2)+1][(GRID_LENGTH//2)-1] = 1
	grid[(GRID_LENGTH//2)+1][(GRID_LENGTH//2)+1] = 1
	grid[(GRID_LENGTH//2)+2][GRID_LENGTH//2]     = 1
	return grid
	
#--Oscillating(repeating pattern)--
def pattern_blinker(grid):
	grid[GRID_LENGTH//2][GRID_LENGTH//2]     = 1
	grid[(GRID_LENGTH//2)+1][GRID_LENGTH//2] = 1
	grid[(GRID_LENGTH//2)-1][GRID_LENGTH//2] = 1
	return grid
	
def pattern_toad(grid):
	grid[GRID_LENGTH//2][GRID_LENGTH//2]         = 1
	grid[(GRID_LENGTH//2)+1][GRID_LENGTH//2]     = 1
	grid[(GRID_LENGTH//2)+1][(GRID_LENGTH//2)-1] = 1
	grid[(GRID_LENGTH//2)+1][(GRID_LENGTH//2)+1] = 1
	grid[GRID_LENGTH//2][(GRID_LENGTH//2)+1]     = 1
	grid[GRID_LENGTH//2][(GRID_LENGTH//2)+2]     = 1
	return grid
	
def pattern_beacon(grid):
	grid[(GRID_LENGTH//2)-1][GRID_LENGTH//2]     = 1
	grid[(GRID_LENGTH//2)-1][(GRID_LENGTH//2)-1] = 1
	grid[GRID_LENGTH//2][(GRID_LENGTH//2)-1]     = 1
	grid[(GRID_LENGTH//2)+1][(GRID_LENGTH//2)+2] = 1
	grid[(GRID_LENGTH//2)+2][(GRID_LENGTH//2)+2] = 1
	grid[(GRID_LENGTH//2)+2][(GRID_LENGTH//2)+1] = 1
	return grid
	
#--Mobile(simulates motion)--
def pattern_glider(grid):
	grid[(GRID_LENGTH//2)+1][GRID_LENGTH//2]     = 1
	grid[(GRID_LENGTH//2)+1][(GRID_LENGTH//2)+1] = 1
	grid[GRID_LENGTH//2][(GRID_LENGTH//2)+1]     = 1
	grid[GRID_LENGTH//2][(GRID_LENGTH//2)-1]     = 1
	grid[(GRID_LENGTH//2)-1][(GRID_LENGTH//2)+1] = 1
	return grid

def pattern_spaceship(grid):
	grid[GRID_LENGTH//2][GRID_LENGTH//2]         = 1
	grid[GRID_LENGTH//2][(GRID_LENGTH//2)-1]     = 1
	grid[GRID_LENGTH//2][(GRID_LENGTH//2)+1]     = 1
	grid[GRID_LENGTH//2][(GRID_LENGTH//2)+2]     = 1
	grid[(GRID_LENGTH//2)-1][(GRID_LENGTH//2)+2] = 1
	grid[(GRID_LENGTH//2)-1][(GRID_LENGTH//2)-2] = 1
	grid[(GRID_LENGTH//2)-2][(GRID_LENGTH//2)+2] = 1
	grid[(GRID_LENGTH//2)-3][(GRID_LENGTH//2)+1] = 1
	grid[(GRID_LENGTH//2)-3][(GRID_LENGTH//2)-2] = 1
	return grid
	
#--Randomized(Primary initialization for Game of Life)--
def pattern_random(grid):
	for i in range(len(grid)):
		for j in range(len(grid)):
			grid[i][j] = random.randint(0,1)
	return grid

#--Empty(Produces an empty grid)
def pattern_empty(grid):
	return grid
	
#Parameters for grid and screen size
GRID_LENGTH   = 80
GRID_SIZE     = 10
SCREEN_WIDTH  = GRID_LENGTH*(GRID_SIZE)
SCREEN_HEIGHT = SCREEN_WIDTH
	
	
if __name__ == '__main__':
#Initializations for Pygame elements and screen
	pygame.init()
	size   = SCREEN_WIDTH,SCREEN_HEIGHT
	screen = pygame.display.set_mode(size)
	
#Produce two lists to act as a double buffer which
#	will alternate, rather than constantly making new
#	lists.
	grid      = generate_grid(GRID_LENGTH,pattern_random)	
	temp_grid = generate_grid(GRID_LENGTH,pattern_empty)
	
#Initialise the screen to black
	screen.fill(colors['black'])
	while True:
#Check for events; for now the quit event triggered
#	by closing the window in the OS.
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			
#Get the list of currently pressed keys and check
#	if escape has been hit; exit if so.
		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE]:
			sys.exit()

#Draw the grid each iteration.
		render_grid(screen,grid,GRID_SIZE)
		
#Check for mouse button 1 and 3 and if either
#	is pressed update the grid at the current
#	position of the mouse; button 1 will add;
#	button 3 will remove.
		if pygame.mouse.get_pressed()[0]:
			pos = pygame.mouse.get_pos()
			row = pos[1] // GRID_SIZE
			col = pos[0] // GRID_SIZE
			adjacent = find_neighbors(grid,row,col)
			for adj in adjacent:
				grid[adj[0]][adj[1]] = 1

		if pygame.mouse.get_pressed()[2]:
			pos = pygame.mouse.get_pos()
			row = pos[1] // GRID_SIZE
			col = pos[0] // GRID_SIZE
			adjacent = find_neighbors(grid,row,col)
			for adj in adjacent:
				grid[adj[0]][adj[1]] = 0
			
#Track the current population as the current grid
#	cells are analyzed for the next generation.
		population = 0
		for i in range(GRID_LENGTH):
			for j in range(GRID_LENGTH):
				neighbors = find_neighbors(grid,i,j)
				count = 0
				for k in neighbors:
					if grid[k[0]][k[1]] == 1:
						count += 1
				next_gen = process_cell(grid[i][j],count)
				temp_grid[i][j] = next_gen
				if next_gen == 1:
					population += 1
					
#Swap the list buffers
		temp = grid
		grid = temp_grid
		temp_grid = temp
		
#Display the next fram, and print the current population.
		pygame.display.flip()
		print('Current Population: ',population)

		
