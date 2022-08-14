import pygame

class Cell():
    def __init__(self, col, row, size, total_cols, grid):
        self.col = col
        self.row = row
        self.total_cols = total_cols
        self.size = size
        self.x = col*size
        self.y = row*size
        self.visited = False
        
        self.walls = []
        self.create_walls()

        self.grid = grid
        self.neighbors = []
    
    def show(self, win):
        if self.visited:
            pygame.draw.rect(win, (224, 159, 61), (self.x, self.y, self.size, self.size))

    def show_walls(self, win):
        for wall in self.walls:
            if wall[0]:
                # if wall exists
                pygame.draw.line(win, (255, 255, 255), wall[1], wall[2])
    
    def update_neighbors(self):
        if self.col > 0:
            self.neighbors.append(self.grid[self.row][self.col-1]) # Neighbor to left

        if self.col < self.total_cols-1:
            self.neighbors.append(self.grid[self.row][self.col+1]) # Neighbor to right

        if self.row > 0:
            self.neighbors.append(self.grid[self.row-1][self.col]) # Neighbor above
        
        if self.row < self.total_cols-1:
            self.neighbors.append(self.grid[self.row+1][self.col]) # Neighbor below
    
    def create_walls(self):
        top_wall = [True, (self.x, self.y), (self.x + self.size, self.y)]
        right_wall = [True, (self.x + self.size, self.y), (self.x + self.size, self.y+self.size)]
        bottom_wall = [True, (self.x + self.size, self.y + self.size), (self.x, self.y + self.size)]
        left_wall = [True, (self.x, self.y + self.size), (self.x, self.y)]
        self.walls.extend((top_wall, right_wall, bottom_wall, left_wall))
