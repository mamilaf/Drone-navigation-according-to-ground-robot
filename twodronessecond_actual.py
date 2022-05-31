import pygame

import math

from queue import PriorityQueue

import base64

import numpy as np





WIDTH = 800

WIN = pygame.display.set_mode((WIDTH, WIDTH))

pygame.display.set_caption("A* Path Finding Algorithm")

path = []

RED = (255, 0, 0)

GREEN = (0, 255, 0)

BLUE = (0, 255, 0)

YELLOW = (255, 255, 0)

WHITE = (255, 255, 255)

BLACK = (0, 0, 0)

PURPLE = (128, 0, 128)

ORANGE = (255, 165 ,0)

GREY = (128, 128, 128)

TURQUOISE = (64, 224, 208)



class Node:

	def __init__(self, row, col, width, total_rows):

		self.row = row

		self.col = col

		self.x = row * width

		self.y = col * width

		self.color = WHITE

		self.neighbors = []

		self.width = width

		self.total_rows = total_rows

		



	def get_pos(self):

		return self.row, self.col



	def is_closed(self):

		return self.color == RED



	def is_open(self):

		return self.color == GREEN



	def is_barrier(self):

		return self.color == BLACK



	def is_start(self):

		return self.color == ORANGE



	def is_end(self):

		return self.color == TURQUOISE



	def reset(self):

		self.color = WHITE



	def make_start(self):

		self.color = ORANGE



	def make_closed(self):

		self.color = RED



	def make_open(self):

		self.color = GREEN



	def make_barrier(self):

		self.color = BLACK



	def make_end(self):

		self.color = TURQUOISE



	def make_path(self):

		self.color = PURPLE



	def draw(self, win):

		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	

	def update_neighbors(self, grid):

		self.neighbors = []

		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN

			self.neighbors.append(grid[self.row + 1][self.col])



		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP

			self.neighbors.append(grid[self.row - 1][self.col])



		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT

			self.neighbors.append(grid[self.row][self.col + 1])



		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT

			self.neighbors.append(grid[self.row][self.col - 1])



		if (self.col < self.total_rows - 1 and self.row > 0) and not grid[self.row - 1][self.col +1].is_barrier(): # DOWN LEFT

				self.neighbors.append(grid[self.row - 1][self.col + 1])



		if (self.col > 0 and self.row > 0) and not grid[self.row - 1][self.col - 1].is_barrier(): # UP LEFT

				self.neighbors.append(grid[self.row - 1][self.col - 1])



		if (self.row < self.total_rows - 1 and self.col > 0) and not grid[self.row + 1][self.col - 1].is_barrier(): # UP RIGHT

				self.neighbors.append(grid[self.row + 1][self.col - 1])



		if (self.col < self.total_rows - 1 and self.row < self.total_rows -1) and not grid[self.row + 1][self.col + 1].is_barrier(): # DOWN RIGHT

				self.neighbors.append(grid[self.row + 1][self.col + 1])



	def __lt__(self, other):

		return False





def h(p1, p2):

	x1, y1 = p1

	x2, y2 = p2

	return abs(x1 - x2) + abs(y1 - y2)





def reconstruct_path(came_from, current, draw):

	while current in came_from:

		current = came_from[current]

		current.make_path()

		draw()

		x,y = current.get_pos()

		path.append([x,y])

	path.reverse()

	np.savetxt("pathvalues.csv", path, delimiter=",",fmt='%s')

	pygame.quit()

	print(path)

		



def algorithm(draw, grid, start, end):

	count = 0

	open_set = PriorityQueue()

	open_set.put((0, count, start))

	came_from = {}

	points = {}

	g_score = {node: float("inf") for row in grid for node in row} #Shortest distance from start node to end node

	g_score[start] = 0

	f_score = {node: float("inf") for row in grid for node in row} #How far the end node is

	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	pygame.init()



	while not open_set.empty():

		for event in pygame.event.get():

			if event.type == pygame.QUIT:

				pygame.quit()

				running = False

				

		

		current = open_set.get()[2]

		open_set_hash.remove(current)



		if current == end:

			reconstruct_path(came_from, end, draw)

			end.make_end()

			return True



		for neighbor in current.neighbors:

			temp_g_score = g_score[current] + 1



			if temp_g_score < g_score[neighbor]:

				came_from[neighbor] = current

				g_score[neighbor] = temp_g_score

				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())

				if neighbor not in open_set_hash:

					count += 1

					open_set.put((f_score[neighbor], count, neighbor))

					open_set_hash.add(neighbor)

					neighbor.make_open()



			draw()

			

		if current != start:

			current.make_closed()



	return False





def make_grid(rows, width):

	grid = []

	gap = width // rows

	for i in range(rows):

		grid.append([])

		for j in range(rows):

			node = Node(i, j, gap, rows)

			grid[i].append(node)



	return grid





def draw_grid(win, rows, width):

	gap = width // rows

	for i in range(rows):

		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))

		for j in range(rows):

			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))





def draw(win, grid, rows, width):

	for row in grid:

		for node in row:

			node.draw(win)



	draw_grid(win, rows, width)

	pygame.display.update()





def main(win, width):

	ROWS = 50

	grid = make_grid(ROWS, width)



	start = None

	end = None



	run = True

	pygame.init()



	while run:

		draw(win, grid, ROWS, width)

		for event in pygame.event.get():

			if event.type == pygame.QUIT:

				run = False

			graph_data = open('cordinates_tello.csv','r').read()
			lines = graph_data.split('\n')
			for line in lines[1:]:
				if len(line)>1:
					xi, yi,zi,xf,yf,zf = line.split(' ')
                    



			rowstart = int(xi)



			colstart = int(yi)



			rowstop = int(xf)



			colstop = int(yf)


			print(grid[rowstart][colstart])

			

			

			node = grid[rowstart][colstart]

			start = node

			

			

			start.make_start()

			node = grid[rowstop][colstop]

			end = node

			end.make_end()



			for row in grid:

				for node in row:

					node.update_neighbors(grid)



			algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

	

	pygame.event.clear()

	pygame.event.wait(0)



main(WIN, WIDTH)