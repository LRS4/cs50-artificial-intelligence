import pygame
from queue import PriorityQueue
from gridsquare import GridSquare


def astar_search(draw, grid: list[list[GridSquare]], start: GridSquare, goal: GridSquare):
    """
    A* search algorithm.

    An A* search is like a breadth-first seach, except
    that in each iteration, instead of expanding the cell
    with the shortest path from the origin, we expand the 
    cell with the lowest overall estimated path length -- 
    this is the distance so far (g_score), plus a heuristic
    estimate of the remaining distance (h). This can be expressed 
    as f(n) = g(n) + h(n)

    See for summary of variables https://youtu.be/JtiK0DOeI4A?t=5075
    """
    count = 0
    g_score = {square: float("inf") for row in grid for square in row}
    g_score[start] = 0
    f_score = {square: float("inf") for row in grid for square in row}
    f_score[start] = h(start.get_position(), goal.get_position())

    frontier = PriorityQueue()
    frontier.put((0, count, start))

    while not frontier.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_node = frontier.get()[2]
        
        if current_node == goal:
            reconstruct_path(current_node, draw)
            goal.make_end()
            return True
        
        for neighbour in current_node.neighbours:
            temp_g_score = g_score[current_node] + 1

            if temp_g_score < g_score[neighbour]:
                neighbour.came_from_square = current_node
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_position(), goal.get_position())

                if neighbour not in frontier.queue:
                    count += 1
                    frontier.put((f_score[neighbour], count, neighbour))
                    neighbour.make_open()

        draw()

        if current_node != start:
            current_node.make_closed()

    return False


def h(a, b):
    """
    Heuristic function calculating Manhattan distance 
    from point a to point b grid coordinates.

    See https://youtu.be/alU04hvz6L4?t=504 for more info
    on straight vs diagonal cost

    Args:
      a: a tuple of a grid square coordinate for point a, for example (1, 2)
      b: a tuple of a grid square coordinate for point b, for example (6, 6)
    Returns:
      h_cost: the estimated distance from point a to point b, for example (3, 3)
      
    """
    a_x, a_y = a
    b_x, b_y = b

    x_distance = abs(a_x - b_x)
    y_distance = abs(a_y - b_y)
    
    return x_distance + y_distance


def reconstruct_path(current_node: GridSquare, draw):
    """
    Traverses the travelled path and reconstructs 
    the optimal path from the current node using 
    it's came_from_square 
    """
    while current_node.came_from_square != None:
        current_node = current_node.came_from_square
        current_node.make_path()
        draw()
