def index(x, y, cols):
    return x + y * cols

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x, y = pos
    col = x // gap
    row = y // gap

    return row, col