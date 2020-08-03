"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state() -> list:
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board: list) -> str:
    """
    Returns player who has the next turn on a board.
    """
    count_of_X = sum(tile.count(X) for tile in board)
    count_of_O = sum(tile.count(O) for tile in board)
    return X if count_of_X is 0 or count_of_X == count_of_O else O 


def actions(board: list):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    raise NotImplementedError


def result(board: list, action: tuple):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    raise NotImplementedError


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
