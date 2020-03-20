import pygame, sys, random

colors = {
	'black'  : (0, 0, 0),
	'white'  : (255, 255, 255),
	'red'    : (255, 57, 51),
	'green'  : (22, 238, 35),
	'blue'   : (8, 58, 242),
	'yellow' : (221, 242, 8)
}

def generate_grid(size):
	grid = [0 for x in range(size)]
	grid[size//2] = 1
	return grid
	
def render_grid(surface,grid,generation=0,size=10):
	for i in range(len(grid)):
		if grid[i] == 0:
			color = colors['black']
		else:
			color = colors['white']
		pygame.draw.rect(surface,colors['white'],pygame.Rect((size*i),size+(generation*size),size-(size//5),size))
		pygame.draw.rect(surface,color,pygame.Rect((size*i)+1,(generation*size)+1,size-(size//5)-2,size-2))

def process_cell(grid,index):
	states = {
		'000': 0,
		'001': 1,
		'010': 0,
		'011': 1,
		'100': 1,
		'101': 0,
		'110': 1,
		'111': 0
	}
	if index == 0:
		left = 1
		right = grid[index+1]
	elif index == len(grid)-1:
		left = grid[index-1]
		right = 1
	else:
		left = grid[index-1]
		right = grid[index+1]
	state = str(left)+str(grid[index])+str(right)
	return states[state]
	
#Parameters
GRID_LENGTH = 99
GRID_SIZE = 10
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
	
	
if __name__ == '__main__':
	pygame.init()
	size = SCREEN_WIDTH,SCREEN_HEIGHT
	screen = pygame.display.set_mode(size)
	grid = generate_grid(GRID_LENGTH)
	generation = 0
	
	screen.fill(colors['black'])
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE]:
			sys.exit()
		if generation > 70:
			generation = 0
		render_grid(screen,grid,generation,GRID_SIZE)
		generation += 1
		temp_grid = generate_grid(GRID_LENGTH)
		for i in range(GRID_LENGTH):
			temp_grid[i] = process_cell(grid,i)
		grid = temp_grid
		pygame.display.flip()
		#pygame.time.wait(1)
