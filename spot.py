import pygame
from colors import *

class Spot():
    def __init__(self, col, row, total_cols, size):
        self.col = col
        self.row = row
        self.size = size
        self.x = self.col * size
        self.y = self.row * size
        self.total_cols = total_cols
        self.color = BLACK

        self.start = False
        self.end = False
        self.obstacle = False
        self.open = False
        self.closed = False
        self.path = False

        self.reset()
    
    def make_start(self):
        self.start = True
        self.color = BLUE
    
    def make_end(self):
        self.end = True
        self.color = RED
    
    def make_obstacle(self):
        self.obstacle = True
        self.color = BLACK
    
    def make_open(self):
        self.open = True
        self.color = GREEN
    
    def make_closed(self):
        self.closed = True
        self.color = ORANGE

    def make_path(self):
        self.color = PURPLE
        self.path = True
    
    def highlight(self):
        self.color = GREY
    
    def get_pos(self):
        return (self.col, self.row)
    
    def reset(self):
        self.start = False
        self.end = False
        self.obstacle = False
        self.color = BLACK
    
    def update_neighbors(self, maze_grid, pathfind_grid):
        self.neighbors = []

        if self.col > 0 and not maze_grid[self.row][self.col].walls[3][0]:
            self.neighbors.append(pathfind_grid[self.row][self.col-1]) # Neighbor to left

        if self.col < self.total_cols-1 and not maze_grid[self.row][self.col].walls[1][0]:
            self.neighbors.append(pathfind_grid[self.row][self.col+1]) # Neighbor to right

        if self.row > 0 and not maze_grid[self.row][self.col].walls[0][0]:
            self.neighbors.append(pathfind_grid[self.row-1][self.col]) # Neighbor above
        
        if self.row < self.total_cols-1 and not maze_grid[self.row][self.col].walls[2][0]:
            self.neighbors.append(pathfind_grid[self.row+1][self.col]) # Neighbor below

    def show(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))
    