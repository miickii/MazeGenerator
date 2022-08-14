import pygame
from queue import PriorityQueue
from utils import *

def alg_events(main_start, main_end, rows, width, grid):
    start = main_start
    end = main_end

    if pygame.mouse.get_pressed()[0]: # LEFT
        pos = pygame.mouse.get_pos()
        row, col = get_clicked_pos(pos, rows, width)
        spot = grid[row][col]

        if not start and spot != end:
            start = spot
            spot.make_start()
        elif not end and spot != start:
            end = spot
            spot.make_end()
    
    if pygame.mouse.get_pressed()[2]: # RIGHT
        pos = pygame.mouse.get_pos()
        row, col = get_clicked_pos(pos, rows, width)
        spot = grid[row][col]
        spot.reset()

        if spot == start:
            start = None
        if spot == end:
            end = None
    
    return start, end

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    clock = pygame.time.Clock()
    count = 0
    open_set = PriorityQueue() # Set of all discovered spots

    # Initially the only discovered spot is the start spot
    # The first value in the tuple is the value of the f function.
    open_set.put((0, count, start)) 

    # came_from is a dictionary with each spot, and the spot immediately preceding it
    came_from = {}

    # This is a dictionary where each key is a spot object, and its corresponding value is the g score
    # Each value is set to infinity initially
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0 # Finding the object that is the same as the start object and setting g score to 0
    
    # This is a dictionary where each key is a spot object and its corresponding value is the current best guess for how short the path is going through that spot
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos()) # Finding the object that is the same as the start object and setting g score to 0
    
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        # Because we are using a PriorityQueue we can get the spot with the lowest f value by using get() method
        # The open_set is a set of tuples, and it will look at the first value of the tuple when determining the lowest value
        # We set the current variable to the spot object of that tuple which lies in index [2]
        # The get() method will also remove the tuple from the set, similarly to how pop() method removes and returnes a value
        current = open_set.get()[2]

        open_set_hash.remove(current)
        current.highlight()

        # Checking if current (the spot with the lowest f score) is the end spot, which means the optimal path is found.
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            # For each neighbor we are recording a temporary g score, which is the g score of the current spot + 1, as we have only moved 1 spot.
            temp_g_score = g_score[current] + 1

            # Checking if the temporary g score is lower than the neighbors current g score.
            # We can access the current g score of the neighbor in this way because each key in g_score is a spot object with a key value that is its g score.
            if temp_g_score < g_score[neighbor]:
                # This path to neighbor is better than any previous one. Record it!
                
                # We record the spot that this neighbor came from, which is just the current spot.
                came_from[neighbor] = current

                # Updating the g_score and f_score of neighbor
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        
        draw()
        clock.tick(120)

        if current != start:
            current.make_closed()
    
    return False