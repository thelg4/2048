import numpy as np
from numpy.core.fromnumeric import squeeze

POSS_MOVES = 4
SQUARES = 3
TOTAL_SQUARES = SQUARES * SQUARES

def init_2048():
    board = np.zeros((TOTAL_SQUARES), dtype="int")
    initial_twos = np.random.default_rng().choice(TOTAL_SQUARES, 2, replace=False)
    board[initial_twos] = 2
    board = board.reshape((SQUARES, SQUARES), dtype="int")

    return board

# TODO: push_board_right

# TODO: merge_squares - merges the squares with new scores

# TODO: move_up - moves the squares up

# TODO: move_right - moves the squares right 

# TODO: move_left - moves the squares left

# TODO: move_down - moves the squares down 

# TODO: fixed_move

# TODO: add new tile - adds a new tile to the board

# TODO: check for win - checks to see if the desired score is reached
