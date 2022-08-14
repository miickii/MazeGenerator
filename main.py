from turtle import right
import pygame
import math
import random
import copy
from cell import Cell
from spot import Spot
from utils import index
from pathfind_alg import *
pygame.init()

WIDTH, HEIGHT = 800, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))

class Game():
    def __init__(self, win, width, height):
        self.win = win
        self.clock = pygame.time.Clock()
        self.fps = 200
        self.frames = 0
        self.width = width
        self.height = height
        self.rows = 25
        self.cols = 25
        self.w = self.width // self.cols
        self.bg_color = (0, 0, 0)
        self.running = True
        self.maze_grid, self.pathfind_grid = self.create_grid()
        self.stack = []

        self.populate_neighbors()

        self.start_pos = (0, 0) # Gets the position of that grid cell
        self.end_pos = (self.cols-1, self.rows-1)

        self.is_running_maze = False
        self.maze_layouts = [] # This is a list that will store all the Cell objects of a created maze, for each created maze
        self.active_layout = None
        self.show_layout = False
        self.current_cell = self.maze_grid[0][0] # Gets the first Cell object of the grid
        self.current_cell.visited = True


        # A* pathfinding algorithm variables
        self.is_running_pathfind = False
        self.start = None
        self.end = None
    
    def run(self):
        while self.running:
            self.frames += 1
            self.handle_events()
            self.update()
            self.clear_screen()
            self.draw()

            #self.clock.tick(self.fps)
        
        pygame.quit()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.start, self.end = alg_events(self.start, self.end, self.rows, self.width, self.pathfind_grid)

            if event.type == pygame.KEYDOWN:
                if not self.is_running_maze:
                    if event.key == pygame.K_SPACE:
                        self.reset()
                        self.is_running_maze = True
                    if not self.is_running_pathfind:
                        if event.key == pygame.K_TAB:
                            self.combine_mazes()
                        if event.key == pygame.K_0:
                            try:
                                self.active_layout = self.maze_layouts[0]
                            except:
                                print("No layout at pos 0")

                            self.show_layout = True
                        if event.key == pygame.K_1:
                            try:
                                self.active_layout = self.maze_layouts[1]
                            except:
                                print("No layout at pos 1")

                            self.show_layout = True
                        if event.key == pygame.K_2:
                            try:
                                self.active_layout = self.maze_layouts[2]
                            except:
                                print("No layout at pos 2")

                            self.show_layout = True
                        if event.key == pygame.K_3:
                            try:
                                self.active_layout = self.maze_layouts[3]
                            except:
                                print("No layout at pos 3")
                            self.show_layout = True
                        
                    if event.key == pygame.K_LALT and self.start and self.end and not self.is_running_maze:
                        for row in range(self.rows):
                            for spot in self.pathfind_grid[row]:
                                spot.update_neighbors(self.maze_grid, self.pathfind_grid)
                        algorithm(lambda: self.draw(), self.pathfind_grid, self.start, self.end)
                        # Only show path
                        for row in range(self.rows):
                            for spot in self.pathfind_grid[row]:
                                if not spot.path:
                                    spot.reset()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_0 or event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3:
                    self.show_layout = False

    
    def update(self):
        if self.is_running_maze:
            #print(self.frames)
            self.run_maze_generator()
            
    def run_maze_generator(self):
        unvisited_neighbors = []
        for neighbor in self.current_cell.neighbors:
            if not neighbor.visited:
                unvisited_neighbors.append(neighbor)
        
        if len(unvisited_neighbors) > 0:
            next_cell = unvisited_neighbors[random.randint(0, len(unvisited_neighbors)-1)]
            self.stack.append(self.current_cell)
            self.remove_wall(self.current_cell, next_cell)
            self.current_cell = next_cell
            self.current_cell.visited = True
        elif len(self.stack) > 0:
            self.current_cell = self.stack.pop()
        else:
            self.is_running_maze = False
            '''maze_grid = []
            for row in range(self.rows):
                maze_grid.append([])
                for cell in self.maze_grid[row]:
                    # Make a copy of the Cell object in that position and add it to the maze_grid
                    cell_copy = copy.deepcopy(cell)
                    maze_grid[row].append(cell_copy)
            self.maze_layouts.append(maze_grid)
            self.active_layout = maze_grid'''



    def draw(self):
        # pygame.draw.rect(self.win, (255, 0, 0), (self.end.x, self.end.y, self.end.size, self.end.size))

        '''for neighbor in self.current.neighbors:
            pygame.draw.rect(self.win, (61, 69, 0), (neighbor.x, neighbor.y, neighbor.size, neighbor.size))'''
        
        if not self.show_layout:
            for row in range(self.rows):
                for col in range(self.cols):
                    cell = self.maze_grid[row][col]
                    spot = self.pathfind_grid[row][col]

                    cell.show(self.win)
                    spot.show(self.win)
                    cell.show_walls(self.win)
        else:
            for row in range(len(self.active_layout)):
                for cell in self.active_layout[row]:
                    cell.show(self.win)
                    cell.show_walls(self.win)
        
        pygame.draw.rect(self.win, (61, 69, 224), (self.current_cell.x, self.current_cell.y, self.w, self.w))

        pygame.display.update()

    def clear_screen(self):
        self.win.fill(self.bg_color)
    
    def create_grid(self):
        maze_grid = []
        pathfind_grid = []
        for row in range(self.rows):
            maze_grid.append([])
            pathfind_grid.append([])
            for col in range(self.cols):
                # populate both the maze and pathfind grids with Cell and Spot objects
                maze_grid[row].append(Cell(col, row, self.w, self.cols, maze_grid))
                pathfind_grid[row].append(Spot(col, row, self.cols, self.w))
        
        return maze_grid, pathfind_grid
    
    def reset(self):
        self.maze_grid, self.pathfind_grid = self.create_grid()
        self.populate_neighbors()
        self.current_cell = self.maze_grid[0][0]
        self.current_cell.visited = True

        self.start = None
        self.end = None
    
    def remove_wall(self, cell_a, cell_b):
        if cell_a.col - cell_b.col > 0:
            # This means that cell_b is to the left of cell_a
            cell_a.walls[3][0] = False
            cell_b.walls[1][0] = False
        elif cell_a.col - cell_b.col < 0:
            # This means that cell_b is to the rigth of cell_a
            cell_a.walls[1][0] = False
            cell_b.walls[3][0] = False
        elif cell_a.row - cell_b.row > 0:
            # This means that cell_b is above cell_a
            cell_a.walls[0][0] = False
            cell_b.walls[2][0] = False
        else:
            # cell_b is below cell_a
            cell_a.walls[2][0] = False
            cell_b.walls[0][0] = False
    
    def populate_neighbors(self):
        # Populate the neigbors array for each cell
        for row in range(self.rows):
            for cell in self.maze_grid[row]:
                cell.update_neighbors()
    
    def combine_mazes(self):
        for row in range(self.rows):
            for col in range(self.cols):
                cell = Cell(col, row, self.w, self.cols, self.maze_grid)
                top_wall = True
                right_wall = True
                bottom_wall = True
                left_wall = True

                # Here we are checking through each layout, and if the cell at col, row has empty walls, then the combined maze should not have those walls
                for layout in self.maze_layouts:
                    if not layout[row][col].walls[0][0]:
                        top_wall = False
                    if not layout[row][col].walls[1][0]:
                        right_wall = False
                    if not layout[row][col].walls[2][0]:
                        bottom_wall = False
                    if not layout[row][col].walls[3][0]:
                        left_wall = False
                
                cell.walls[0][0] = top_wall
                cell.walls[1][0] = right_wall
                cell.walls[2][0] = bottom_wall
                cell.walls[3][0] = left_wall

                self.maze_grid[row][col] = cell


if __name__ == "__main__":
    game = Game(window, WIDTH, HEIGHT)
    game.run()
