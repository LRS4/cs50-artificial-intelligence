"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state() -> list:
    """
    Returns starting state of the board.
    """
    return [[X, EMPTY, EMPTY],
            [EMPTY, O, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board: list) -> str:
    """
    Returns player who has the next turn on a board.
    In the initial game state, X gets the first move. 
    Subsequently, the player alternates with each additional move.
    """
    count_of_X = sum(row.count(X) for row in board)
    count_of_O = sum(row.count(O) for row in board)
    return X if count_of_X is 0 or count_of_X == count_of_O else O 


def actions(board: list) -> set:
    """
    Returns set of all possible actions (i, j) available on the board.
    i corresponds to the row of the move (0, 1, or 2).
    j corresponds to which cell/tile in the row corresponds to the move (also 0, 1, or 2).
    Possible moves are any cells on the board that do not already have an X or an O in them.
    """
    possible_actions = set()
    empty_cells_matrix = [map(lambda i: i == EMPTY, tile) for tile in board]
    # print([list(cell) for cell in empty_cells_matrix])
    for i, row in enumerate(empty_cells_matrix):
        for j, tile in enumerate(row):
            if tile is True: 
                action = (i, j)
                possible_actions.add(action)
    print(possible_actions)
    return possible_actions


def result(board: list, action: tuple) -> list:
    """
    Returns the board that results from making move (i, j) on the board.
    """
    current_player = player(board)
    new_board = copy.deepcopy(board)
    i, j = action[0], action[1]
    new_board[i][j] = current_player
    print(new_board)
    return new_board


def winner(board: list):
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


def terminal(board: list) -> bool:
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board: list):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board: list):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
