from mdp import MarkovDecisionProcess
from itertools import product
from board import *


class GameBoard(MarkovDecisionProcess):
    def __init__(self, matrix, board_size, win_score):
        # initial state, passed from game instance
        self.initial_state = matrix

        # game parameters
        self.board_size = board_size
        self.win_score = win_score

        # determine all possible values a square can hold
        self.possible_values = []
        possible_value = self.win_score
        while possible_value > 1:
            self.possible_values.append(possible_value)
            possible_value /= 2
        self.possible_values.append(0)

    def get_states(self):
        # get all state permutations given valid square values
        return [[list(i[x:x+self.board_size]) for x in range(0, len(i), self.board_size)] for i in product("01", repeat=pow(self.board_size, 2))]

    def get_initial_state(self):
        return self.initial_state

    def get_legal_actions(self, state):
        legal_actions = []
        if vertical_move_exists(state):
            legal_actions.extend(['up', 'down'])
        if horizontal_move_exists(state):
            legal_actions.extend(['left', 'right'])
        return legal_actions

    # todo: determine possible successor states and probabilities by considering all new tile possibilities after move
    def get_succ_states_and_prob(self, state, action):
        if action == 'left':
            new_state, _ = left(state)
        elif action == 'right':
            new_state, _ = right(state)
        elif action == 'up':
            new_state, _ = up(state)
        elif action == 'down':
            new_state, _ = down(state)
        else:
            print(f'Invalid action: {action}')

    def get_reward(self, state, action, succ):
        if state.is_lose_state():
            return -1
        elif state.is_win_state():
            return 1
        else:
            return 0

    def is_terminal(self, state):
        # a state is terminal if there are no legal moves or the target score has been reached
        return is_lose_state(state) or is_win_state(state, self.win_score)
