import pygame
from colors import colors

class GridSquare():
    def __init__(self, row, column, width, total_rows):
        self.row = row
        self.column = column  
        self.x = row * width 
        self.y = column * width
        self.color = colors["WHITE"]
        self.neighbours = []
        self.width = width 
        self.total_rows = total_rows 
        self.came_from_square: GridSquare = None

    def get_position(self):
        return self.row, self.column

    def is_closed(self):
        return self.color == colors["RED"]

    def is_open(self):
        return self.color == colors["GREEN"]

    def is_barrier(self):
        return self.color == colors["BLACK"]

    def is_start(self):
        return self.color == colors["ORANGE"]

    def is_end(self):
        return self.color == colors["TURQUOISE"]

    def make_start(self):
        self.color = colors["ORANGE"]

    def reset(self):
        self.color = colors["WHITE"]

    def make_closed(self):
        self.color = colors["RED"]

    def make_open(self):
        self.color = colors["GREEN"]

    def make_barrier(self):
        self.color = colors["BLACK"]

    def make_end(self):
        self.color = colors["TURQUOISE"]

    def make_path(self):
        self.color = colors["PURPLE"]

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []

        # UP
        if self.row > 0 and not grid[self.row - 1][self.column].is_barrier(): 
            self.neighbours.append(grid[self.row - 1][self.column])

        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.column].is_barrier(): 
            self.neighbours.append(grid[self.row + 1][self.column])

        # RIGHT
        if self.column < self.total_rows - 1 and not grid[self.row][self.column + 1].is_barrier(): 
            self.neighbours.append(grid[self.row][self.column + 1])

        # LEFT
        if self.column > 0 and not grid[self.row][self.column - 1].is_barrier(): 
            self.neighbours.append(grid[self.row][self.column - 1])

        # UP LEFT
        if self.row > 0 and self.column > 0 \
            and not grid[self.row - 1][self.column - 1].is_barrier():
            self.neighbours.append(grid[self.row - 1][self.column - 1])

        # UP RIGHT
        if self.row > 0 and self.column < self.total_rows - 1 \
            and not grid[self.row - 1][self.column + 1].is_barrier():
            self.neighbours.append(grid[self.row - 1][self.column + 1])

        # DOWN RIGHT 
        if self.row < self.total_rows - 1 \
            and self.column < self.total_rows - 1 \
            and not grid[self.row + 1][self.column + 1].is_barrier(): 
            self.neighbours.append(grid[self.row + 1][self.column + 1])

        # DOWN LEFT
        if self.row < self.total_rows - 1 \
            and self.column > 0 \
            and not grid[self.row + 1][self.column -1].is_barrier():
            self.neighbours.append(grid[self.row + 1][self.column -1])





    def __lt__(self, another_grid_square):
        return False