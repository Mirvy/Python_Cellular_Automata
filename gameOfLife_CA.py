import pygame, sys, random

colors = {
	'black'  : (0, 0, 0),
	'white'  : (255, 255, 255),
	'red'    : (255, 57, 51),
	'green'  : (22, 238, 35),
	'blue'   : (8, 58, 242),
	'yellow' : (221, 242, 8)
}


def generate_grid(size,callback):
	grid = [[0 for x in range(size)] for y in range(size)]
	#grid[size//2] = 1
	#grid = [random.randint(0,1) for x in range(size)]
	grid = callback(grid)
	return grid
	
def render_grid(surface,grid,size=10):
	for i in range(len(grid)):
		for j in range(len(grid)):
			if grid[i][j] == 0:
				color = colors['black']
			else:
				color = colors['white']
			pygame.draw.rect(
				surface,
				colors['white'],
				pygame.Rect(
					(size*j),
					size+(i*size),
					size-(size//5),
					size)
				)
			pygame.draw.rect(
				surface,
				color,
				pygame.Rect(
				(size*j)+1,
				(i*size)+1,
				size-(size//5)-2,
				size-2)
			)

def find_neighbors(grid,row,col):
	count = 0
	if 0 < row < len(grid)-1 and 0 < col < len(grid)-1:
		if grid[row+1][col+1] == 1: count +=1
		if grid[row][col+1]   == 1: count +=1
		if grid[row-1][col+1] == 1: count +=1
		if grid[row+1][col]   == 1: count +=1
		if grid[row-1][col]   == 1: count +=1
		if grid[row+1][col-1] == 1: count +=1
		if grid[row][col-1]   == 1: count +=1
		if grid[row-1][col-1] == 1: count +=1
	return count
	
def process_cell(cell_state,neighbor_count):
	if cell_state == 1 and (neighbor_count >= 4 or neighbor_count <= 1):
		return 0
	if cell_state == 0 and neighbor_count == 3:
		return 1
	return cell_state
	
#Pattern Initialization Callbacks
#Static
def pattern_block(grid):
	grid[GRID_LENGTH//2][GRID_LENGTH//2] = 1
	grid[GRID_LENGTH//2][(GRID_LENGTH//2)+1] = 1
	grid[(GRID_LENGTH//2)+1][GRID_LENGTH//2] = 1
	grid[(GRID_LENGTH//2)+1][(GRID_LENGTH//2)+1] = 1
	return grid
	
def pattern_loaf(grid):
	grid[(GRID_LENGTH//2)-1][GRID_LENGTH//2] = 1
	grid[(GRID_LENGTH//2)-1][(GRID_LENGTH//2)-1] = 1
	grid[GRID_LENGTH//2][(GRID_LENGTH//2)-2] = 1
	grid[GRID_LENGTH//2][(GRID_LENGTH//2)+1] = 1
	grid[(GRID_LENGTH//2)+1][(GRID_LENGTH//2)-1] = 1
	grid[(GRID_LENGTH//2)+1][(GRID_LENGTH//2)+1] = 1
	grid[(GRID_LENGTH//2)+2][GRID_LENGTH//2] = 1
	return grid
	
#Oscillating
def pattern_blinker(grid):
	grid[GRID_LENGTH//2][GRID_LENGTH//2] = 1
	grid[(GRID_LENGTH//2)+1][GRID_LENGTH//2] = 1
	grid[(GRID_LENGTH//2)-1][GRID_LENGTH//2] = 1
	return grid
	
def pattern_toad(grid):
	grid[GRID_LENGTH//2][GRID_LENGTH//2] = 1
	grid[(GRID_LENGTH//2)+1][GRID_LENGTH//2] = 1
	grid[(GRID_LENGTH//2)+1][(GRID_LENGTH//2)-1] = 1
	grid[(GRID_LENGTH//2)+1][(GRID_LENGTH//2)+1] = 1
	grid[GRID_LENGTH//2][(GRID_LENGTH//2)+1] = 1
	grid[GRID_LENGTH//2][(GRID_LENGTH//2)+2] = 1
	return grid
	
def pattern_beacon(grid):
	grid[(GRID_LENGTH//2)-1][GRID_LENGTH//2] = 1
	grid[(GRID_LENGTH//2)-1][(GRID_LENGTH//2)-1] = 1
	grid[GRID_LENGTH//2][(GRID_LENGTH//2)-1] = 1
	grid[(GRID_LENGTH//2)+1][(GRID_LENGTH//2)+2] = 1
	grid[(GRID_LENGTH//2)+2][(GRID_LENGTH//2)+2] = 1
	grid[(GRID_LENGTH//2)+2][(GRID_LENGTH//2)+1] = 1
	return grid
	
#Mobile 
def pattern_glider(grid):
	grid[(GRID_LENGTH//2)+1][GRID_LENGTH//2] = 1
	grid[(GRID_LENGTH//2)+1][(GRID_LENGTH//2)+1] = 1
	grid[GRID_LENGTH//2][(GRID_LENGTH//2)+1] = 1
	grid[GRID_LENGTH//2][(GRID_LENGTH//2)-1] = 1
	grid[(GRID_LENGTH//2)-1][(GRID_LENGTH//2)+1] = 1
	return grid

def pattern_spaceship(grid):
	grid[GRID_LENGTH//2][GRID_LENGTH//2] = 1
	grid[GRID_LENGTH//2][(GRID_LENGTH//2)-1] = 1
	grid[GRID_LENGTH//2][(GRID_LENGTH//2)+1] = 1
	grid[GRID_LENGTH//2][(GRID_LENGTH//2)+2] = 1
	grid[(GRID_LENGTH//2)-1][(GRID_LENGTH//2)+2] = 1
	grid[(GRID_LENGTH//2)-1][(GRID_LENGTH//2)-2] = 1
	grid[(GRID_LENGTH//2)-2][(GRID_LENGTH//2)+2] = 1
	grid[(GRID_LENGTH//2)-3][(GRID_LENGTH//2)+1] = 1
	grid[(GRID_LENGTH//2)-3][(GRID_LENGTH//2)-2] = 1
	return grid
	
#Randomized
def pattern_random(grid):
	for i in range(len(grid)):
		for j in range(len(grid)):
			grid[i][j] = random.randint(0,1)
	return grid

#Empty
def pattern_empty(grid):
	return grid
	
#Parameters
GRID_LENGTH = 63
GRID_SIZE = 14
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
	
	
if __name__ == '__main__':
	pygame.init()
	size = SCREEN_WIDTH,SCREEN_HEIGHT
	screen = pygame.display.set_mode(size)
	grid = generate_grid(GRID_LENGTH,pattern_random)	
	
	screen.fill(colors['black'])
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE]:
			sys.exit()
		render_grid(screen,grid,GRID_SIZE)
		temp_grid = generate_grid(GRID_LENGTH,pattern_empty)
		for i in range(GRID_LENGTH):
			for j in range(GRID_LENGTH):
				neighbors = find_neighbors(grid,i,j)
				print('row:%d ,col:%d ,neighbour_count:%d'%(i,j,neighbors))
				temp_grid[i][j] = process_cell(grid[i][j],neighbors)
		grid = temp_grid
		pygame.display.flip()
		print(grid[GRID_LENGTH-1][0])
		#pygame.time.wait(60)
		
