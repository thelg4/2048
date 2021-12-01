from mdp import MarkovDecisionProcess
from itertools import product, chain
from matrix import *
from copy import deepcopy


class GameBoard(MarkovDecisionProcess):
    def __init__(self, board_size, win_score):
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
        return [tuple(map(tuple, [list(i[x:x+self.board_size]) for x in range(0, len(i), self.board_size)])) for i in product(self.possible_values, repeat=pow(self.board_size, 2))
                if not all([v == 0 for v in i]) and not list(i).count(self.win_score) > self.board_size]

    def get_win_states(self):
        return [state for state in self.get_states() if is_win_state(state, self.win_score)]

    def get_lose_states(self):
        return [state for state in self.get_states() if is_lose_state(state)]

    def get_legal_actions(self, state):
        if self.is_terminal(state):
            return []

        legal_actions = []
        if vertical_move_exists(state):
            legal_actions.extend(['up', 'down'])
        if horizontal_move_exists(state):
            legal_actions.extend(['left', 'right'])
        return legal_actions

    def get_succ_states_and_prob(self, state, action):
        if self.is_terminal(state):
            return []

        # calculate new state after move
        if action == 'left':
            state, _ = left(state)
        elif action == 'right':
            state, _ = right(state)
        elif action == 'up':
            state, _ = up(state)
        elif action == 'down':
            state, _ = down(state)
        else:
            print(f'Invalid action: {action}')

        # create separate successor state for each empty space being filled by either 2 or 4
        succ_states_and_prob = []
        num_zero_squares = list(chain.from_iterable(state)).count(0)
        for i, row in enumerate(state):
            for j, v in enumerate(row):
                if v == 0:
                    succ_state_2 = deepcopy(state)
                    succ_state_2[i][j] = 2
                    succ_state_2_tup = tuple(map(tuple, succ_state_2))
                    succ_states_and_prob.append((succ_state_2_tup, 0.9/num_zero_squares))

                    succ_state_4 = deepcopy(state)
                    succ_state_4[i][j] = 4
                    succ_state_4_tup = tuple(map(tuple, succ_state_4))
                    succ_states_and_prob.append((succ_state_4_tup, 0.1/num_zero_squares))
        return succ_states_and_prob

    def get_reward(self, state, action, succ):
        if is_lose_state(state):
            return -1
        elif is_win_state(state, self.win_score):
            return 1
        else:
            return 0

    def is_terminal(self, state):
        # a state is terminal if there are no legal moves or the target score has been reached
        return is_lose_state(state) or is_win_state(state, self.win_score)
