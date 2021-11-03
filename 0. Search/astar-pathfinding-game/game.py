import pygame
from gridsquare import GridSquare
from colors import colors
from astar import astar_search

WIDTH = 800
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")


def make_grid(rows: int, width: float) -> list[list[GridSquare]]:
    """
    Creates the game grid as a 2D array of 
    GridSquare objects.
    """
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            square = GridSquare(row=i, 
                                column=j,
                                width=gap,
                                total_rows=rows)
            grid[i].append(square)
    
    return grid


def draw_gridlines(window, rows, width):
    """
    For every row draw an horizontal line 
    and vertical line on the grid.
    """
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, colors["GRAY"], (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(window, colors["GRAY"], (j * gap, 0), (j * gap, width))


def draw(window, grid, rows, width):
    """
    Draw the grid at every frame. Paints the 
    canvas white then redraws the grid squares
    with their current state and the gridlines
    """
    window.fill(colors["WHITE"])

    for row in grid:
        for square in row:
            square.draw(window)

    draw_gridlines(window, rows, width)
    pygame.display.update()


def get_clicked_square(position, rows, width):
    """
    Determines what grid square was clicked on
    """
    gap = width // rows
    y, x = position

    row = y // gap
    column = x // gap

    return row, column
        

def main(window, width):
    rows = 50
    grid = make_grid(rows, width)
    start: GridSquare = None
    end: GridSquare = None
    game_is_running = True
    search_algorithm_is_running = False

    while game_is_running:
        draw(window, grid, rows, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if search_algorithm_is_running:
                continue

            if pygame.mouse.get_pressed()[0]:
                mouse_position = pygame.mouse.get_pos()
                row, column = get_clicked_square(mouse_position, rows, width)
                square: GridSquare = grid[row][column]
                if not start and square != end:
                    start = square
                    start.make_start()
                elif not end and square != start:
                    end = square
                    end.make_end()
                elif square != end and square != start:
                    square.make_barrier()
            elif pygame.mouse.get_pressed()[2]:
                mouse_position = pygame.mouse.get_pos()
                row, column = get_clicked_square(mouse_position, rows, width)
                square: GridSquare = grid[row][column]
                square.reset()
                if square == start:
                    start = None
                
                if square == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for row in grid:
                        for square in row:
                            square.update_neighbours(grid)

                    astar_search(lambda: draw(window, grid, rows, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None 
                    grid = make_grid(rows, width)
            
    pygame.quit()


if __name__ == "__main__":
    main(WINDOW, WIDTH)